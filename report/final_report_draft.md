# Do Price and Volume Signals Predict Short-Term Stock Outperformance?

## Problem Statement

This project asks whether historical price and volume patterns can predict which U.S. stocks and ETFs will outperform over the next five trading days. This question matters because investors, analysts, and researchers often use technical indicators such as momentum, volatility, and abnormal volume, but many apparent trading signals disappear after careful testing. Our goal is not to claim that stock prices can be predicted perfectly. Instead, we test whether common price-volume signals contain measurable information in a rigorous, reproducible, leak-free data science workflow.

Rather than forecasting the exact future price of a single company, we frame the project as a cross-sectional ranking problem: on each trading date, can we identify the assets most likely to rank in the top 20% of future five-day returns? This is closer to a real investment decision, where an analyst chooses among many possible assets at the same point in time.

## Data Description

The data comes from the Kaggle Huge Stock Market Dataset by Boris Marjanovic. It contains historical daily price and volume data for U.S. stocks and ETFs listed on NYSE, NASDAQ, and NYSE MKT. Each file includes `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, and `OpenInt`. The prices are adjusted for dividends and splits, which makes return calculations more meaningful over long periods.

The full downloaded archive contains 17,078 price files. For the main analysis, we use a liquid research universe of large stocks and major ETFs to keep the analysis reproducible on a laptop while still studying a broad set of assets. The pipeline loaded 1,412,252 raw rows. After filtering for sufficient trading history, average volume, valid prices, and non-penny-stock price levels, the final cleaned universe contained 230 assets and 1,345,128 daily observations. After feature engineering and target construction, the modeling dataset contained 679,803 asset-date rows.

Important limitations include the dataset ending in 2017, possible survivorship bias, lack of sector and fundamental data, lack of news or macroeconomic variables, and simplified transaction cost assumptions. The results should be interpreted as an empirical data science study, not as investment advice.

## Methods

We combine individual CSV files into a long asset-date panel. Invalid rows are removed if prices are missing or nonpositive, if volume is negative, or if the reported high price is lower than the low price. We then filter to assets with at least three years of data, average daily volume above 100,000, and median price above $5.

All engineered features are based only on information available at date `t`. The main feature groups are:

- Lagged returns over 1, 5, 21, and 63 trading days.
- Rolling volatility over 5, 21, and 63 trading days.
- Abnormal volume, including volume ratio and volume z-score.
- Liquidity, measured by log dollar volume.
- Intraday and overnight price behavior, including daily range, open-to-close return, and gap return.
- Trend and risk features, including moving-average distance and 63-day drawdown.
- Market context, using SPY when available.

The main target is `top_quintile_next_5d`, which equals 1 if an asset ranks in the top 20% of future five-day returns among assets available on the same date. We split the data by time rather than using random sampling. The default split trains on observations through 2012, validates on 2013-2014, and tests after 2014. This prevents future information from entering the training process.

We compare two machine learning models with simple baselines. The models are logistic regression and histogram gradient boosting. Baselines include a market benchmark, a 21-day momentum strategy, and a short-term reversal strategy. Classification performance is evaluated with ROC-AUC and average precision. We also run a simple equal-weight backtest that selects the top 25 assets by predicted probability, subtracts a 0.10% transaction cost, and compares cumulative returns and risk-adjusted performance.

## Findings

The models show measurable predictive power on the held-out test period. Logistic regression achieved a test ROC-AUC of 0.628, while histogram gradient boosting achieved a test ROC-AUC of 0.635. Because a random classifier would have ROC-AUC near 0.50, these results suggest that price and volume features contain weak but real information about short-term relative performance.

The strongest logistic regression features were market volatility, 63-day drawdown, 21-day volatility, distance from the 63-day moving average, and daily high-low range. This suggests that risk, trend position, and market regime mattered more than raw recent return alone.

The momentum quintile analysis produced a surprising result. Assets in the lowest past-21-day momentum quintile had the highest average future five-day return, while assets in the highest past-21-day momentum quintile had the lowest average future five-day return. In this universe and horizon, the evidence favored short-term reversal more than simple continuation momentum.

The backtest results were mixed, which is realistic for financial data. Histogram gradient boosting produced the highest average five-day return among active strategies and an annualized return estimate of 14.6%, but it also had higher volatility and a large maximum drawdown. The market benchmark had a lower annualized return estimate of 11.8% but the strongest Sharpe ratio at 1.03. Logistic regression beat the simple momentum strategy but did not beat the market benchmark on risk-adjusted return.

Key generated figures:

![Distribution of daily returns](../figures/eda_returns_distribution.png)

![Future five-day return by past momentum quintile](../figures/momentum_quintiles.png)

![Model comparison by test ROC-AUC](../figures/model_comparison.png)

![Cumulative return of test-period strategies](../figures/backtest_cumulative_returns.png)

![Most important logistic regression features](../figures/feature_importance.png)

## Conclusions

Historical price and volume signals can help rank short-term stock and ETF performance better than random chance, but the signal is weak and not automatically profitable after risk and transaction costs. The strongest evidence from this study is not that a simple trading rule can reliably beat the market, but that a careful data science workflow can separate measurable patterns from overconfident claims.

The project also shows why financial modeling requires special care. Random train-test splits would overstate performance; exact price prediction would be unstable; and model accuracy alone would not reveal whether a strategy is economically useful. Time-based validation, baseline comparison, feature interpretation, and backtesting all matter.

Future work could improve the study by adding sector labels, firm fundamentals, macroeconomic indicators, news sentiment, updated post-2017 prices, delisted securities, more realistic transaction costs, and walk-forward retraining. A stronger version could also compare stocks and ETFs separately or analyze performance across market regimes.

## Reflection

Each team member should add a short paragraph before submission describing their contribution, what surprised them, and what they would do differently next time. Suggested reflection themes include the complexity of cleaning large financial datasets, the importance of avoiding look-ahead bias, the difference between classification performance and portfolio performance, and the value of clear GitHub organization in team data science work.
