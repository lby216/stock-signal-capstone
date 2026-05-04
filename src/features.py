from __future__ import annotations

import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "ret_1d",
    "ret_5d",
    "ret_21d",
    "ret_63d",
    "volatility_5d",
    "volatility_21d",
    "volatility_63d",
    "volume_ratio_21d",
    "volume_zscore_63d",
    "dollar_volume_log",
    "daily_range",
    "open_close_return",
    "gap_return",
    "price_vs_ma_21d",
    "price_vs_ma_63d",
    "drawdown_63d",
    "market_ret_5d",
    "market_volatility_21d",
    "excess_ret_5d",
]


def add_features(panel: pd.DataFrame, market_ticker: str = "SPY") -> pd.DataFrame:
    """Create leak-free lagged features and future return targets."""
    df = panel.sort_values(["Ticker", "Date"]).copy()
    grouped = df.groupby("Ticker", group_keys=False)

    df["ret_1d"] = grouped["Close"].pct_change(1)
    df["ret_5d"] = grouped["Close"].pct_change(5)
    df["ret_21d"] = grouped["Close"].pct_change(21)
    df["ret_63d"] = grouped["Close"].pct_change(63)

    df["volatility_5d"] = grouped["ret_1d"].rolling(5).std().reset_index(level=0, drop=True)
    df["volatility_21d"] = grouped["ret_1d"].rolling(21).std().reset_index(level=0, drop=True)
    df["volatility_63d"] = grouped["ret_1d"].rolling(63).std().reset_index(level=0, drop=True)

    volume_ma_21 = grouped["Volume"].rolling(21).mean().reset_index(level=0, drop=True)
    volume_std_63 = grouped["Volume"].rolling(63).std().reset_index(level=0, drop=True)
    volume_ma_63 = grouped["Volume"].rolling(63).mean().reset_index(level=0, drop=True)
    df["volume_ratio_21d"] = df["Volume"] / volume_ma_21
    df["volume_zscore_63d"] = (df["Volume"] - volume_ma_63) / volume_std_63
    df["dollar_volume_log"] = np.log1p(df["Close"] * df["Volume"])

    df["daily_range"] = (df["High"] - df["Low"]) / df["Close"]
    df["open_close_return"] = df["Close"] / df["Open"] - 1
    df["gap_return"] = df["Open"] / grouped["Close"].shift(1) - 1

    ma_21 = grouped["Close"].rolling(21).mean().reset_index(level=0, drop=True)
    ma_63 = grouped["Close"].rolling(63).mean().reset_index(level=0, drop=True)
    rolling_max_63 = grouped["Close"].rolling(63).max().reset_index(level=0, drop=True)
    df["price_vs_ma_21d"] = df["Close"] / ma_21 - 1
    df["price_vs_ma_63d"] = df["Close"] / ma_63 - 1
    df["drawdown_63d"] = df["Close"] / rolling_max_63 - 1

    df["future_ret_5d"] = grouped["Close"].shift(-5) / df["Close"] - 1

    market = (
        df[df["Ticker"].eq(market_ticker)][["Date", "ret_5d", "volatility_21d", "future_ret_5d"]]
        .rename(
            columns={
                "ret_5d": "market_ret_5d",
                "volatility_21d": "market_volatility_21d",
                "future_ret_5d": "future_market_ret_5d",
            }
        )
        .drop_duplicates("Date")
    )
    if market.empty:
        market = (
            df.groupby("Date")
            .agg(
                market_ret_5d=("ret_5d", "median"),
                market_volatility_21d=("volatility_21d", "median"),
                future_market_ret_5d=("future_ret_5d", "median"),
            )
            .reset_index()
        )

    df = df.merge(market, on="Date", how="left")
    df["excess_ret_5d"] = df["ret_5d"] - df["market_ret_5d"]
    df["future_excess_ret_5d"] = df["future_ret_5d"] - df["future_market_ret_5d"]

    df["future_rank_pct"] = df.groupby("Date")["future_ret_5d"].rank(pct=True, method="average")
    df["top_quintile_next_5d"] = (df["future_rank_pct"] >= 0.80).astype(int)
    df["outperform_market_next_5d"] = (df["future_excess_ret_5d"] > 0).astype(int)

    df = df.replace([np.inf, -np.inf], np.nan)
    return df


def modeling_frame(feature_panel: pd.DataFrame) -> pd.DataFrame:
    required = FEATURE_COLUMNS + ["future_ret_5d", "top_quintile_next_5d"]
    return feature_panel.dropna(subset=required).copy()

