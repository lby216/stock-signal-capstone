from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .features import FEATURE_COLUMNS


@dataclass(frozen=True)
class TimeSplit:
    train_end: str = "2012-12-31"
    validation_end: str = "2014-12-31"


def time_split(df: pd.DataFrame, split: TimeSplit = TimeSplit()) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dates = pd.to_datetime(df["Date"])
    train = df[dates <= pd.Timestamp(split.train_end)].copy()
    valid = df[(dates > pd.Timestamp(split.train_end)) & (dates <= pd.Timestamp(split.validation_end))].copy()
    test = df[dates > pd.Timestamp(split.validation_end)].copy()

    if min(len(train), len(valid), len(test)) == 0:
        unique_dates = sorted(pd.to_datetime(df["Date"]).unique())
        first_cut = unique_dates[int(len(unique_dates) * 0.60)]
        second_cut = unique_dates[int(len(unique_dates) * 0.80)]
        train = df[pd.to_datetime(df["Date"]) <= first_cut].copy()
        valid = df[(pd.to_datetime(df["Date"]) > first_cut) & (pd.to_datetime(df["Date"]) <= second_cut)].copy()
        test = df[pd.to_datetime(df["Date"]) > second_cut].copy()
    return train, valid, test


def build_models(random_state: int = 498) -> dict[str, Pipeline]:
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state)),
            ]
        ),
        "hist_gradient_boosting": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        max_iter=80,
                        learning_rate=0.06,
                        max_leaf_nodes=31,
                        l2_regularization=0.05,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }


def sample_training_rows(df: pd.DataFrame, max_rows: int = 120_000, random_state: int = 498) -> pd.DataFrame:
    """Keep model fitting responsive while preserving class balance."""
    if len(df) <= max_rows:
        return df
    return (
        df.groupby("top_quintile_next_5d", group_keys=False)
        .apply(lambda part: part.sample(min(len(part), max_rows // 2), random_state=random_state))
        .sample(frac=1, random_state=random_state)
        .reset_index(drop=True)
    )


def evaluate_predictions(y_true: pd.Series, score: np.ndarray) -> dict[str, float]:
    pred = (score >= np.nanmedian(score)).astype(int)
    metrics = {
        "accuracy_at_median_cutoff": accuracy_score(y_true, pred),
        "average_precision": average_precision_score(y_true, score),
    }
    if y_true.nunique() == 2:
        metrics["roc_auc"] = roc_auc_score(y_true, score)
    else:
        metrics["roc_auc"] = np.nan
    return metrics


def train_and_score(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Pipeline]]:
    train, valid, test = time_split(df)
    train_valid = pd.concat([train, valid], ignore_index=True)
    models = build_models()

    rows = []
    scored_parts = []
    for name, model in models.items():
        train_fit = sample_training_rows(train)
        train_valid_fit = sample_training_rows(train_valid)

        model.fit(train_fit[FEATURE_COLUMNS], train_fit["top_quintile_next_5d"])
        valid_score = model.predict_proba(valid[FEATURE_COLUMNS])[:, 1]
        rows.append({"model": name, "split": "validation", **evaluate_predictions(valid["top_quintile_next_5d"], valid_score)})

        model.fit(train_valid_fit[FEATURE_COLUMNS], train_valid_fit["top_quintile_next_5d"])
        test_score = model.predict_proba(test[FEATURE_COLUMNS])[:, 1]
        rows.append({"model": name, "split": "test", **evaluate_predictions(test["top_quintile_next_5d"], test_score)})

        scored = test[["Date", "Ticker", "AssetType", "future_ret_5d", "future_market_ret_5d"]].copy()
        scored["model"] = name
        scored["score"] = test_score
        scored_parts.append(scored)

    metrics = pd.DataFrame(rows)
    scored_predictions = pd.concat(scored_parts, ignore_index=True)
    return metrics, scored_predictions, models


def feature_importance(models: dict[str, Pipeline]) -> pd.DataFrame:
    rows = []
    for name, model in models.items():
        estimator = model.named_steps["model"]
        if hasattr(estimator, "feature_importances_"):
            values = estimator.feature_importances_
        elif hasattr(estimator, "coef_"):
            values = np.abs(estimator.coef_[0])
        else:
            continue
        rows.extend({"model": name, "feature": feature, "importance": value} for feature, value in zip(FEATURE_COLUMNS, values))
    return pd.DataFrame(rows).sort_values(["model", "importance"], ascending=[True, False])
