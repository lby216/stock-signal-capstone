from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd

os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))

from .backtest import baseline_strategies, performance_summary, top_n_strategy
from .clean_data import clean_price_panel, make_universe_summary
from .features import add_features, modeling_frame
from .generate_sample_data import generate_sample_data
from .load_data import discover_price_files, load_from_raw_dir
from .modeling import feature_importance, train_and_score
from .visualization import (
    save_backtest_chart,
    save_feature_importance,
    save_model_comparison,
    save_momentum_quintile_chart,
    save_returns_distribution,
)


def read_ticker_file(path: str | None) -> list[str] | None:
    if not path:
        return None
    ticker_path = Path(path)
    if not ticker_path.exists():
        raise FileNotFoundError(f"Ticker file does not exist: {ticker_path}")
    return [
        line.strip().upper()
        for line in ticker_path.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def run(
    raw_dir: str,
    output_dir: str,
    ticker_file: str | None = None,
    use_sample_if_missing: bool = True,
    save_panels: bool = False,
) -> None:
    project_root = Path(output_dir)
    data_processed = project_root / "data" / "processed"
    figures = project_root / "figures"
    data_processed.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    raw_path = Path(raw_dir)
    if not discover_price_files(raw_path) and use_sample_if_missing:
        print("No Kaggle files found. Generating sample data for a reproducible smoke test.")
        generate_sample_data(project_root / "data" / "sample")
        raw_path = project_root / "data" / "sample"

    tickers = read_ticker_file(ticker_file)
    raw = load_from_raw_dir(raw_path, tickers=tickers)
    print(f"Loaded raw rows: {len(raw):,}", flush=True)
    clean = clean_price_panel(raw)
    print(f"Clean rows: {len(clean):,}; assets retained: {clean['Ticker'].nunique():,}", flush=True)
    universe = make_universe_summary(clean)
    features = add_features(clean)
    print("Feature engineering complete.", flush=True)
    frame = modeling_frame(features)
    print(f"Modeling rows: {len(frame):,}", flush=True)

    if save_panels:
        raw.to_parquet(data_processed / "raw_panel.parquet", index=False)
        clean.to_parquet(data_processed / "clean_panel.parquet", index=False)
        features.to_parquet(data_processed / "feature_panel.parquet", index=False)
        frame.to_parquet(data_processed / "modeling_frame.parquet", index=False)
    universe.to_csv(data_processed / "universe_summary.csv", index=False)

    save_returns_distribution(features, figures / "eda_returns_distribution.png")
    momentum_summary = save_momentum_quintile_chart(frame, figures / "momentum_quintiles.png")
    momentum_summary.to_csv(data_processed / "momentum_quintile_summary.csv", index=False)
    print("EDA figures complete.", flush=True)

    metrics, scored, models = train_and_score(frame)
    importance = feature_importance(models)
    metrics.to_csv(data_processed / "model_metrics.csv", index=False)
    scored.to_csv(data_processed / "test_predictions.csv", index=False)
    importance.to_csv(data_processed / "feature_importance.csv", index=False)
    print("Models complete.", flush=True)

    test_dates = pd.to_datetime(scored["Date"]).drop_duplicates()
    strategy_frames = [top_n_strategy(scored, model_name=name) for name in scored["model"].unique()]
    strategy_frames.append(baseline_strategies(frame, test_dates))
    strategies = pd.concat(strategy_frames, ignore_index=True).sort_values(["model", "Date"])
    summary = performance_summary(strategies)
    strategies.to_csv(data_processed / "strategy_returns.csv", index=False)
    summary.to_csv(data_processed / "strategy_performance_summary.csv", index=False)

    save_model_comparison(metrics, figures / "model_comparison.png")
    save_backtest_chart(strategies, figures / "backtest_cumulative_returns.png")
    save_feature_importance(importance, figures / "feature_importance.png")
    print("Backtest and figures complete.", flush=True)

    print("Pipeline complete.")
    print(f"Assets retained: {universe['Ticker'].nunique():,}")
    print(f"Modeling rows: {len(frame):,}")
    print(summary.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="data/raw", help="Directory containing Kaggle Stocks/ and ETFs/ folders.")
    parser.add_argument("--output-dir", default=".", help="Project root where outputs should be written.")
    parser.add_argument("--ticker-file", default=None, help="Optional newline-delimited ticker universe.")
    parser.add_argument("--no-sample", action="store_true", help="Fail instead of generating sample data when raw files are absent.")
    parser.add_argument("--save-panels", action="store_true", help="Save large intermediate parquet panels.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(
        args.raw_dir,
        args.output_dir,
        ticker_file=args.ticker_file,
        use_sample_if_missing=not args.no_sample,
        save_panels=args.save_panels,
    )
