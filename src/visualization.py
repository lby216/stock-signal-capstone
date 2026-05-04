from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def set_style() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")


def save_returns_distribution(df: pd.DataFrame, out_path: str | Path) -> None:
    set_style()
    sample = df["ret_1d"].dropna().clip(-0.20, 0.20)
    if len(sample) > 250_000:
        sample = sample.sample(250_000, random_state=498)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(sample, bins=100, color="#4477AA", edgecolor="white", linewidth=0.2)
    ax.set_title("Distribution of Daily Returns")
    ax.set_xlabel("Daily return, clipped to [-20%, 20%]")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def save_momentum_quintile_chart(df: pd.DataFrame, out_path: str | Path) -> pd.DataFrame:
    set_style()
    temp = df.dropna(subset=["ret_21d", "future_ret_5d"]).copy()
    rank_pct = temp.groupby("Date")["ret_21d"].rank(pct=True, method="first")
    temp["momentum_quintile"] = pd.cut(
        rank_pct,
        bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
        labels=["Q1 losers", "Q2", "Q3", "Q4", "Q5 winners"],
        include_lowest=True,
    )
    summary = temp.groupby("momentum_quintile", observed=True).agg(mean_future_5d_return=("future_ret_5d", "mean")).reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary["momentum_quintile"].astype(str), summary["mean_future_5d_return"], color="#4477AA")
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("Future 5-Day Return by Past 21-Day Momentum Quintile")
    ax.set_xlabel("")
    ax.set_ylabel("Mean future 5-day return")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return summary


def save_model_comparison(metrics: pd.DataFrame, out_path: str | Path) -> None:
    set_style()
    fig, ax = plt.subplots(figsize=(8, 5))
    temp = metrics[metrics["split"].eq("test")]
    ax.bar(temp["model"], temp["roc_auc"], color="#228833")
    ax.axhline(0.5, color="black", linestyle="--", linewidth=1)
    ax.set_title("Test ROC-AUC by Model")
    ax.set_xlabel("")
    ax.set_ylabel("ROC-AUC")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def save_backtest_chart(strategy_returns: pd.DataFrame, out_path: str | Path) -> None:
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5))
    for model, group in strategy_returns.groupby("model"):
        ax.plot(group["Date"], group["cumulative_return"], label=model)
    ax.legend()
    ax.set_title("Cumulative Return of Test-Period Strategies")
    ax.set_xlabel("")
    ax.set_ylabel("Cumulative return")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def save_feature_importance(importance: pd.DataFrame, out_path: str | Path, model_name: str = "logistic_regression") -> None:
    set_style()
    temp = importance[importance["model"].eq(model_name)].head(12).copy()
    temp = temp.sort_values("importance")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(temp["feature"], temp["importance"], color="#CC6677")
    ax.set_title(f"Top Feature Importances: {model_name}")
    ax.set_xlabel("Importance")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
