# Do Price and Volume Signals Predict Short-Term Stock Outperformance?

**DATA 498D Capstone Project**

**Team Members:** Qifan Wang · Chenyao Qu · Boyang Li · Jiaheng Xie · Zhiyuan Lin

---

## Problem Statement

This project asks whether historical price and volume patterns can predict which U.S. stocks and ETFs will outperform over the next five trading days. This question matters because investors, analysts, and researchers often use technical indicators such as momentum, volatility, and abnormal volume, but many apparent trading signals disappear after careful testing. Our goal is not to claim that stock prices can be predicted perfectly. Instead, we test whether common price-volume signals contain measurable information in a rigorous, reproducible, leak-free data science workflow.

Rather than forecasting the exact future price of a single company, we frame the project as a cross-sectional ranking problem: on each trading date, can we identify the assets most likely to rank in the top 20% of future five-day returns? This is closer to a real investment decision, where an analyst chooses among many possible assets at the same point in time.

---

## Data Description

The data comes from the Kaggle Huge Stock Market Dataset by Boris Marjanovic. It contains historical daily price and volume data for U.S. stocks and ETFs listed on NYSE, NASDAQ, and NYSE MKT. Each file includes `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, and `OpenInt`. The prices are adjusted for dividends and splits, which makes return calculations more meaningful over long periods.

The full downloaded archive contains 17,078 price files. For the main analysis, we use a liquid research universe of large stocks and major ETFs to keep the analysis reproducible on a laptop while still studying a broad set of assets. The pipeline loaded 1,412,252 raw rows. After filtering for sufficient trading history, average volume, valid prices, and non-penny-stock price levels, the final cleaned universe contained 230 assets and 1,345,128 daily observations. After feature engineering and target construction, the modeling dataset contained 679,803 asset-date rows.

Important limitations include the dataset ending in 2017, possible survivorship bias, lack of sector and fundamental data, lack of news or macroeconomic variables, and simplified transaction cost assumptions. The results should be interpreted as an empirical data science study, not as investment advice.

---

## Methods

We combine individual CSV files into a long asset-date panel. Invalid rows are removed if prices are missing or nonpositive, if volume is negative, or if the reported high price is lower than the low price. We then filter to assets with at least three years of data, average daily volume above 100,000, and median price above $5.

All engineered features are based only on information available at date `t`. The main feature groups are:

- **Momentum:** Lagged returns over 1, 5, 21, and 63 trading days.
- **Risk:** Rolling volatility over 5, 21, and 63 trading days.
- **Volume:** Abnormal volume, including volume ratio and volume z-score.
- **Liquidity:** Log dollar volume.
- **Price behavior:** Intraday daily range, open-to-close return, and gap return.
- **Trend & drawdown:** Moving-average distance (21d, 63d) and 63-day drawdown.
- **Market context:** SPY return and volatility when available.

The main target is `top_quintile_next_5d`, which equals 1 if an asset ranks in the top 20% of future five-day returns among assets available on the same date. We split the data by time rather than using random sampling. The default split trains on observations through 2012, validates on 2013--2014, and tests after 2014. This prevents future information from entering the training process.

We compare two machine learning models with simple baselines. The models are logistic regression and histogram gradient boosting. Baselines include a market benchmark, a 21-day momentum strategy, and a short-term reversal strategy. Classification performance is evaluated with ROC-AUC and average precision. We also run a simple equal-weight backtest that selects the top 25 assets by predicted probability, subtracts a 0.10% transaction cost, and compares cumulative returns and risk-adjusted performance.

---

## Findings

Figure 1 shows the distribution of daily returns across the liquid universe. Returns are tightly concentrated near zero with heavier tails on both sides, which reflects the noisy nature of short-horizon equity returns.

![Figure 1: Distribution of daily returns](figures/eda_returns_distribution.png)
*Figure 1: Distribution of daily returns across the liquid universe.*

The momentum quintile analysis produced a surprising result. Assets in the lowest past-21-day momentum quintile had the highest average future five-day return, while assets in the highest past-21-day momentum quintile had the lowest average future five-day return. In this universe and horizon, the evidence favored short-term reversal more than simple continuation momentum (Figure 2).

![Figure 2: Momentum quintile test](figures/momentum_quintiles.png)
*Figure 2: Future five-day return by past 21-day momentum quintile. Q1 (lowest past return) shows the highest forward return, indicating short-term reversal dominates in this universe.*

The models show measurable predictive power on the held-out test period. Logistic regression achieved a test ROC-AUC of 0.628, while histogram gradient boosting achieved a test ROC-AUC of 0.635. Because a random classifier would have ROC-AUC near 0.50, these results suggest that price and volume features contain weak but real information about short-term relative performance (Figure 3).

![Figure 3: Model comparison](figures/model_comparison.png)
*Figure 3: Model comparison by test-period ROC-AUC. Both models exceed the random baseline of 0.50.*

The backtest results were mixed, which is realistic for financial data. Histogram gradient boosting produced the highest average five-day return among active strategies and an annualized return estimate of 14.6%, but it also had higher volatility and a large maximum drawdown. The market benchmark had a lower annualized return estimate of 11.8% but the strongest Sharpe ratio at 1.03. Logistic regression beat the simple momentum strategy but did not beat the market benchmark on risk-adjusted return (Figure 4).

![Figure 4: Backtest cumulative returns](figures/backtest_cumulative_returns.png)
*Figure 4: Cumulative return of test-period strategies. The market benchmark achieves the best Sharpe ratio despite a lower raw return than histogram gradient boosting.*

The strongest logistic regression features were market volatility, 63-day drawdown, 21-day volatility, distance from the 63-day moving average, and daily high-low range. This suggests that risk, trend position, and market regime mattered more than raw recent return alone (Figure 5).

![Figure 5: Feature importance](figures/feature_importance.png)
*Figure 5: Most important logistic regression features. Market volatility and drawdown dominate, suggesting regime and risk features carry the most signal.*

---

## Conclusions

Historical price and volume signals can help rank short-term stock and ETF performance better than random chance, but the signal is weak and not automatically profitable after risk and transaction costs. The strongest evidence from this study is not that a simple trading rule can reliably beat the market, but that a careful data science workflow can separate measurable patterns from overconfident claims.

The project also shows why financial modeling requires special care. Random train-test splits would overstate performance; exact price prediction would be unstable; and model accuracy alone would not reveal whether a strategy is economically useful. Time-based validation, baseline comparison, feature interpretation, and backtesting all matter.

Future work could improve the study by adding sector labels, firm fundamentals, macroeconomic indicators, news sentiment, updated post-2017 prices, delisted securities, more realistic transaction costs, and walk-forward retraining. A stronger version could also compare stocks and ETFs separately or analyze performance across market regimes.

---

## Reflection

**Qifan Wang** *(Data Acquisition & Cleaning)*

Working with the raw Kaggle archive turned out to be far more labor-intensive than I anticipated. The 17,078 individual CSV files had inconsistent column formatting, and building a reliable pipeline to validate prices (catching negative volumes, impossible high-low inversions, and stale rows) required far more iteration than the EDA itself. What surprised me most was how many seemingly complete price files had to be discarded due to insufficient trading history or penny-stock price levels. If I were to do this again, I would document each filtering decision with an explicit count of rows dropped and the reason, so the cleaning logic is transparent and auditable at every step rather than condensed into a single summary statistic.

**Chenyao Qu** *(Exploratory Analysis & Visualization)*

Creating the EDA visualizations forced me to think carefully about what "informative" actually means for a panel spanning hundreds of assets over more than a decade. The daily return distribution looked deceptively well-behaved in aggregate, but broke down significantly at the individual asset level, a reminder that aggregate summaries can mask important heterogeneity. I was also struck by how strongly the momentum quintile chart contradicted my prior assumptions: the lowest-momentum group showed the highest forward returns, which directly challenges the standard trend-following narrative. If I were to redo this project, I would invest more time in visualizing asset-level variation and time-varying patterns rather than relying primarily on cross-sectional averages.

**Boyang Li** *(Feature Engineering & Baseline Modeling)*

Building the feature engineering module reinforced what turned out to be the most critical lesson of the entire project: every feature must be constructed using only information available at decision time `t`. What looks like a simple lagged return becomes a potential source of look-ahead bias if the window is not carefully aligned relative to the prediction date. Establishing the logistic regression baseline before any complex modeling was also essential: it created a clear interpretable benchmark and prevented the team from over-claiming based on black-box outputs. If I were starting over, I would also implement a Fama-MacBeth style cross-sectional regression to decompose return predictability more formally and provide stronger statistical grounding for the signal estimates.

**Jiaheng Xie** *(Machine Learning & Evaluation)*

Evaluating the histogram gradient boosting model showed me that statistical performance and economic performance are genuinely different things. An ROC-AUC of 0.635 is meaningful given the signal-to-noise ratio in financial returns, yet when we translated that into a backtest, the active strategy underperformed the market on a risk-adjusted basis. This gap between classification skill and portfolio utility was the project's most important practical insight. I was also surprised by how sensitive feature importance rankings were to minor changes in model specification. In future work I would use SHAP values to produce more stable and interpretable feature attributions, and add a probability calibration step to ensure the model's output scores are well-behaved before they are used for portfolio ranking.

**Zhiyuan Lin** *(Repository, Report & Presentation)*

Coordinating the GitHub repository and integrating outputs from four analytical workstreams showed me that version control discipline matters as much as modeling quality in a team data science project. Decisions that seem minor, including consistent file naming, clear commit messages, and modular code in `src/`, had an outsized effect on whether the team could reproduce results without friction. What surprised me most was how much the final presentation challenged us to translate technical findings into a clear narrative. The honest conclusion that signals are real but modest, and that a passive market benchmark has a better Sharpe ratio, is actually harder to communicate credibly than an overconfident claim would have been. Next time I would set up a shared project board from day one to track task dependencies explicitly.
