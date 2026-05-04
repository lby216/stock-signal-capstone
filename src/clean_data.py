from __future__ import annotations

import pandas as pd


def clean_price_panel(
    panel: pd.DataFrame,
    min_history_days: int = 756,
    min_avg_volume: float = 100_000,
    min_median_price: float = 5.0,
) -> pd.DataFrame:
    """Clean and filter the raw price panel for liquid, analyzable assets."""
    df = panel.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"])
    df = df[(df["Open"] > 0) & (df["High"] > 0) & (df["Low"] > 0) & (df["Close"] > 0)]
    df = df[(df["Volume"] >= 0) & (df["High"] >= df["Low"])]
    df = df.sort_values(["Ticker", "Date"]).drop_duplicates(["Ticker", "Date"], keep="last")

    stats = (
        df.groupby("Ticker")
        .agg(
            n_days=("Date", "size"),
            avg_volume=("Volume", "mean"),
            median_price=("Close", "median"),
            first_date=("Date", "min"),
            last_date=("Date", "max"),
        )
        .reset_index()
    )
    eligible = stats[
        (stats["n_days"] >= min_history_days)
        & (stats["avg_volume"] >= min_avg_volume)
        & (stats["median_price"] >= min_median_price)
    ]["Ticker"]

    df = df[df["Ticker"].isin(eligible)].copy()
    return df.reset_index(drop=True)


def make_universe_summary(clean_panel: pd.DataFrame) -> pd.DataFrame:
    return (
        clean_panel.groupby(["Ticker", "AssetType"], dropna=False)
        .agg(
            first_date=("Date", "min"),
            last_date=("Date", "max"),
            n_days=("Date", "size"),
            avg_volume=("Volume", "mean"),
            median_price=("Close", "median"),
        )
        .reset_index()
        .sort_values(["AssetType", "Ticker"])
    )

