# Contributions Revised

This revised contribution file lists the actual team member names and aligns the responsibilities with the final report reflection section.

| Team Member | Primary Role | Detailed Contributions |
|---|---|---|
| Qifan Wang | Data Acquisition & Cleaning | Downloaded and organized the Kaggle Huge Stock Market Dataset; helped validate raw daily price and volume files; supported the cleaning pipeline that removed invalid prices, negative volumes, high-low inconsistencies, insufficient-history assets, low-volume assets, and penny-stock observations; documented key data limitations and filtering decisions used in the final report. |
| Chenyao Qu | Exploratory Analysis & Visualization | Created exploratory summaries for the asset-date panel; analyzed daily return distributions, data coverage, price and volume behavior, and missingness patterns; produced and interpreted the return distribution figure and the momentum quintile visualization; helped explain how aggregate return patterns can hide asset-level differences. |
| Boyang Li | Feature Engineering & Baseline Modeling | Built the feature engineering workflow for lagged returns, rolling volatility, abnormal volume, liquidity, moving-average distance, drawdown, intraday range, gap return, and market-context features; ensured features used only information available at decision date `t`; implemented baseline modeling with logistic regression and helped interpret feature importance. |
| Jiaheng Xie | Machine Learning & Evaluation | Trained and evaluated the histogram gradient boosting model; compared model performance against logistic regression and baseline strategies; analyzed test-period ROC-AUC, average precision, and feature importance behavior; helped connect classification performance to economic backtest performance and identified limits of model usefulness. |
| Zhiyuan Lin | Repository, Report & Presentation | Coordinated the GitHub repository structure, file naming, and reproducibility materials; integrated outputs from data cleaning, EDA, feature engineering, modeling, and backtesting into the final report; assembled final figures and presentation materials; helped communicate the main conclusion that price-volume signals are measurable but modest and should be interpreted carefully. |

All team members contributed to the written final report, final presentation preparation, peer feedback, and project revision process.
