# Notebook Guide

The final submission can use one notebook or several notebooks. The recommended notebook sequence is:

1. `01_data_cleaning.ipynb`
   - Load Kaggle CSV files.
   - Explain dataset source and columns.
   - Clean invalid rows and filter to a liquid research universe.
   - Save `data/processed/clean_panel.parquet`.

2. `02_eda.ipynb`
   - Show number of assets over time.
   - Plot daily return distribution.
   - Plot volume distribution on log scale.
   - Compare stocks and ETFs if both are available.
   - Discuss outliers and limitations.

3. `03_feature_engineering.ipynb`
   - Explain each lagged feature.
   - Create future five-day return target.
   - Demonstrate that features use only past information.
   - Save `data/processed/modeling_frame.parquet`.

4. `04_modeling.ipynb`
   - Use time-based train, validation, and test splits.
   - Train logistic regression and random forest.
   - Compare against random, momentum, and reversal baselines.
   - Save model metrics and feature importance.

5. `05_backtest_and_results.ipynb`
   - Rank assets by predicted probability.
   - Select the top 25 assets.
   - Compare cumulative return, Sharpe ratio, max drawdown, and win rate.
   - Export final report figures.

For a single reproducible run, use:

```bash
python -m src.run_pipeline --raw-dir data/raw --output-dir .
```

