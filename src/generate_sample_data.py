from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_sample_data(out_dir: str | Path = "data/sample", n_tickers: int = 80, random_state: int = 498) -> None:
    """Create a small fake stock universe so the pipeline can be smoke-tested without Kaggle files."""
    rng = np.random.default_rng(random_state)
    out_path = Path(out_dir) / "Stocks"
    out_path.mkdir(parents=True, exist_ok=True)

    dates = pd.bdate_range("2010-01-01", "2017-11-10")
    market_shock = rng.normal(0.00025, 0.009, len(dates))
    for i in range(n_tickers):
        ticker = "SPY" if i == 0 else f"STK{i:03d}"
        beta = 1.0 if ticker == "SPY" else rng.normal(1.0, 0.25)
        idio = rng.normal(0.0001, rng.uniform(0.010, 0.030), len(dates))
        returns = beta * market_shock + idio
        close = 30 * np.exp(np.cumsum(returns))
        open_price = close * (1 + rng.normal(0, 0.003, len(dates)))
        high = np.maximum(open_price, close) * (1 + rng.uniform(0, 0.012, len(dates)))
        low = np.minimum(open_price, close) * (1 - rng.uniform(0, 0.012, len(dates)))
        volume = rng.lognormal(mean=12.2, sigma=0.7, size=len(dates)).astype(int)
        df = pd.DataFrame(
            {
                "Date": dates.strftime("%Y-%m-%d"),
                "Open": open_price,
                "High": high,
                "Low": low,
                "Close": close,
                "Volume": volume,
                "OpenInt": 0,
            }
        )
        df.to_csv(out_path / f"{ticker}.csv", index=False)


if __name__ == "__main__":
    generate_sample_data()

