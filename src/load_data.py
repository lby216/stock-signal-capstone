from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = {"Date", "Open", "High", "Low", "Close", "Volume"}


def discover_price_files(raw_dir: str | Path) -> list[Path]:
    """Find Kaggle stock/ETF CSV files under a raw data directory."""
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        return []

    files = []
    for pattern in ("Stocks/*.txt", "ETFs/*.txt", "Stocks/*.csv", "ETFs/*.csv", "*.txt", "*.csv"):
        files.extend(raw_path.glob(pattern))
    return sorted(set(files))


def filter_files_by_tickers(files: Iterable[Path], tickers: Iterable[str]) -> list[Path]:
    wanted = {ticker.strip().upper() for ticker in tickers if ticker.strip()}
    return [file_path for file_path in files if ticker_from_path(file_path) in wanted]


def ticker_from_path(path: Path) -> str:
    return path.stem.upper().replace(".US", "")


def asset_type_from_path(path: Path) -> str:
    parent = path.parent.name.lower()
    if parent == "etfs":
        return "ETF"
    if parent == "stocks":
        return "Stock"
    return "Unknown"


def read_price_file(path: str | Path) -> pd.DataFrame:
    """Read one Kaggle price file and attach ticker metadata."""
    path = Path(path)
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    keep_cols = [col for col in ["Date", "Open", "High", "Low", "Close", "Volume", "OpenInt"] if col in df.columns]
    df = df[keep_cols].copy()
    df["Ticker"] = ticker_from_path(path)
    df["AssetType"] = asset_type_from_path(path)
    return df


def load_price_panel(files: Iterable[str | Path]) -> pd.DataFrame:
    frames = []
    for file_path in files:
        try:
            frames.append(read_price_file(file_path))
        except Exception as exc:
            print(f"Skipping {file_path}: {exc}")

    if not frames:
        raise FileNotFoundError(
            "No valid price files were found. Put Kaggle files under data/raw/Stocks and data/raw/ETFs."
        )

    return pd.concat(frames, ignore_index=True)


def load_from_raw_dir(raw_dir: str | Path, tickers: Iterable[str] | None = None) -> pd.DataFrame:
    files = discover_price_files(raw_dir)
    if tickers is not None:
        files = filter_files_by_tickers(files, tickers)
    return load_price_panel(files)
