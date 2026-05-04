# Recorded Presentation Outline

Target length: 8-12 minutes.

## 1. Opening and Research Question

State the project question:

Can historical price and volume patterns predict which U.S. stocks and ETFs will outperform over the next five trading days?

Explain why the topic matters and why the team framed the task as cross-sectional outperformance rather than exact price prediction.

## 2. Data

Introduce the Kaggle Huge Stock Market Dataset.

Mention:

- U.S. stocks and ETFs
- Daily prices and volume
- Adjusted prices
- Data ends in 2017
- Important limitations

Show a data coverage or return distribution figure.

## 3. Feature Engineering

Explain the main feature groups:

- Momentum: trailing returns
- Risk: rolling volatility and drawdown
- Volume: abnormal volume and dollar volume
- Price behavior: gap return, daily range, moving-average distance

Emphasize that all features use only information available at date `t`.

## 4. Modeling

Explain the target:

An asset is labeled positive if it falls in the top 20% of future five-day returns on that date.

Describe:

- Time-based train, validation, and test split
- Logistic regression
- Random forest
- Momentum and reversal baselines

Show model comparison figure.

## 5. Backtest

Explain the simple strategy:

- Rank assets by model probability
- Select top 25
- Equal-weight portfolio
- Hold for five trading days
- Compare to benchmark and simple baselines

Show cumulative return and performance summary.

## 6. Main Findings

Summarize what the real-data run shows:

- Which signals were most important
- Whether model performance exceeded random
- Whether ML improved over simple momentum
- Whether transaction costs reduced gains

## 7. Limitations and Next Steps

Mention:

- Historical dataset only through 2017
- Possible survivorship bias
- No fundamentals, sectors, macro data, or news
- Simplified transaction costs
- Backtests do not guarantee future performance

## 8. Team Reflection

Each member briefly states their contribution and one thing learned.

