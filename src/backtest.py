from __future__ import annotations

import numpy as np
import pandas as pd


def top_n_strategy(
    scored: pd.DataFrame,
    model_name: str,
    n_assets: int = 25,
    transaction_cost: float = 0.001,
) -> pd.DataFrame:
    model_scores = scored[scored["model"].eq(model_name)].copy()
    model_scores["rank"] = model_scores.groupby("Date")["score"].rank(ascending=False, method="first")
    selected = model_scores[model_scores["rank"] <= n_assets].copy()

    returns = selected.groupby("Date").agg(strategy_ret_5d=("future_ret_5d", "mean")).reset_index()
    returns["strategy_ret_5d_after_cost"] = returns["strategy_ret_5d"] - transaction_cost
    returns["model"] = model_name
    returns["cumulative_return"] = (1 + returns["strategy_ret_5d_after_cost"]).cumprod() - 1
    return returns


def baseline_strategies(feature_df: pd.DataFrame, test_dates: pd.Series, n_assets: int = 25) -> pd.DataFrame:
    df = feature_df[feature_df["Date"].isin(pd.to_datetime(test_dates).unique())].copy()
    rows = []
    for signal, name, ascending in [
        ("ret_21d", "momentum_top_21d", False),
        ("ret_5d", "short_term_reversal", True),
    ]:
        temp = df.dropna(subset=[signal, "future_ret_5d"]).copy()
        temp["rank"] = temp.groupby("Date")[signal].rank(ascending=ascending, method="first")
        chosen = temp[temp["rank"] <= n_assets]
        returns = chosen.groupby("Date").agg(strategy_ret_5d=("future_ret_5d", "mean")).reset_index()
        returns["model"] = name
        rows.append(returns)

    benchmark = df.groupby("Date").agg(strategy_ret_5d=("future_market_ret_5d", "median")).reset_index()
    benchmark["model"] = "market_benchmark"
    rows.append(benchmark)

    out = pd.concat(rows, ignore_index=True)
    out["strategy_ret_5d_after_cost"] = np.where(out["model"].eq("market_benchmark"), out["strategy_ret_5d"], out["strategy_ret_5d"] - 0.001)
    out["cumulative_return"] = out.groupby("model")["strategy_ret_5d_after_cost"].transform(lambda s: (1 + s).cumprod() - 1)
    return out


def performance_summary(strategy_returns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model, group in strategy_returns.groupby("model"):
        r = group["strategy_ret_5d_after_cost"].dropna()
        if r.empty:
            continue
        periods_per_year = 252 / 5
        annual_return = (1 + r.mean()) ** periods_per_year - 1
        annual_volatility = r.std() * np.sqrt(periods_per_year)
        sharpe = annual_return / annual_volatility if annual_volatility else np.nan
        cumulative = (1 + r).cumprod()
        drawdown = cumulative / cumulative.cummax() - 1
        rows.append(
            {
                "model": model,
                "mean_5d_return": r.mean(),
                "annualized_return": annual_return,
                "annualized_volatility": annual_volatility,
                "sharpe_ratio": sharpe,
                "max_drawdown": drawdown.min(),
                "win_rate": (r > 0).mean(),
            }
        )
    return pd.DataFrame(rows).sort_values("sharpe_ratio", ascending=False)

