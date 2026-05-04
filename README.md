# Price and Volume Signals in U.S. Stocks and ETFs

DATA 498D Capstone Project

## Project Question

Can historical price and volume patterns predict which U.S. stocks and ETFs will outperform over the next five trading days?

This project studies whether lagged returns, volatility, abnormal volume, moving-average distance, and drawdown features contain measurable information about short-term cross-sectional stock performance. Instead of predicting the exact price of one stock, we evaluate whether a model can rank many assets and identify those likely to fall in the top 20% of next-week returns.

## Data Source

The project uses the Kaggle **Huge Stock Market Dataset** by Boris Marjanovic:

https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

The dataset contains historical daily price and volume data for U.S.-based stocks and ETFs trading on NYSE, NASDAQ, and NYSE MKT. The key columns are:

- `Date`
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`
- `OpenInt`

Prices are adjusted for dividends and splits. The dataset is historical and was last updated in 2017, so results should not be interpreted as current trading advice.

## Repository Structure

```text
stock-signal-capstone/
├── README.md
├── CONTRIBUTIONS.md
├── data_dictionary.md
├── requirements.txt
├── data/
│   ├── raw/              # Put Kaggle Stocks/ and ETFs/ folders here
│   ├── sample/           # Generated sample data for smoke testing
│   └── processed/        # Cleaned panels, model outputs, summaries
├── figures/              # Generated figures for report and presentation
├── notebooks/
│   └── analysis_guide.md
├── report/
│   ├── final_report_draft.md
│   └── project_proposal.md
├── presentation/
│   └── presentation_outline.md
└── src/
    ├── load_data.py
    ├── clean_data.py
    ├── features.py
    ├── modeling.py
    ├── backtest.py
    ├── visualization.py
    ├── generate_sample_data.py
    └── run_pipeline.py
```

## How to Run

1. Download the Kaggle dataset.
2. Place the extracted folders here:

```text
data/raw/Stocks/
data/raw/ETFs/
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the full pipeline from the project root:

```bash
python -m src.run_pipeline --raw-dir data/raw --output-dir .
```

If the Kaggle data is not present, the pipeline automatically creates a synthetic sample dataset so the code can be tested end to end:

```bash
python -m src.run_pipeline --raw-dir data/raw --output-dir .
```

To require real Kaggle data and fail if it is absent:

```bash
python -m src.run_pipeline --raw-dir data/raw --output-dir . --no-sample
```

## Methods

The analysis follows a leak-free financial modeling workflow:

1. Load individual stock and ETF files into one long panel.
2. Clean invalid prices, impossible high-low relationships, missing values, and illiquid assets.
3. Engineer only lagged features available at date `t`.
4. Define the target as whether each asset ranks in the top 20% of future five-day returns.
5. Split data by time, not random sampling.
6. Compare simple baselines to logistic regression and random forest models.
7. Backtest a simple equal-weight portfolio using the model's top-ranked assets.
8. Compare performance to market, momentum, and short-term reversal baselines.

## Key Outputs

After running the pipeline, the most important outputs are:

- `data/processed/universe_summary.csv`
- `data/processed/model_metrics.csv`
- `data/processed/strategy_performance_summary.csv`
- `data/processed/feature_importance.csv`
- `figures/eda_returns_distribution.png`
- `figures/momentum_quintiles.png`
- `figures/model_comparison.png`
- `figures/backtest_cumulative_returns.png`
- `figures/feature_importance.png`

## Main Limitations

- The dataset ends in 2017 and is not current.
- The analysis uses price and volume only, not fundamentals, macro variables, options, news, or sentiment.
- Historical backtests do not guarantee future performance.
- Delisting, survivorship bias, and transaction cost assumptions may affect conclusions.
- The simple backtest is educational and does not model slippage, liquidity constraints, taxes, or market impact.

## Project Status

The repository is structured for the final DATA 498D submission. Once the full Kaggle dataset is placed in `data/raw/`, rerun the pipeline and replace sample-based outputs with real-data outputs before submitting.

