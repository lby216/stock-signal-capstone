# Project Proposal

## Problem

We will investigate whether historical price and volume patterns can predict short-term relative performance among U.S. stocks and ETFs. The main research question is: **Can lagged returns, volatility, abnormal volume, moving-average distance, and drawdown features predict whether an asset will rank in the top 20% of future five-day returns?**

This question matters because investors and analysts often rely on technical signals, but many such signals are noisy or unstable. A rigorous data science study can test whether these signals contain measurable predictive information and whether machine learning improves on simple rules such as momentum.

## Dataset

We will use the Kaggle Huge Stock Market Dataset by Boris Marjanovic. It contains historical daily price and volume data for U.S. stocks and ETFs listed on NYSE, NASDAQ, and NYSE MKT. Each file includes `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, and `OpenInt`. Prices are adjusted for dividends and splits.

Known limitations include the dataset ending in 2017, possible survivorship bias, lack of fundamentals or news variables, and the difficulty of modeling realistic transaction costs.

## Planned Analytic Approach

We will combine all individual files into a long stock-date panel, clean invalid observations, and filter to liquid assets with sufficient trading history. We will engineer lagged return, volatility, volume shock, moving-average, gap, intraday range, and drawdown features. Our main target will be whether an asset falls into the top quintile of future five-day returns.

The analysis will include exploratory data analysis, quintile-based statistical tests, logistic regression, random forest modeling, feature importance analysis, and a simple equal-weight backtest. We will split data by time rather than random sampling to avoid look-ahead bias.

## Team Contributions

Each team member will own one major component: data engineering, EDA, feature engineering and statistical testing, modeling, or backtesting and communication. All members will contribute to the final report, recorded presentation, and GitHub repository.

