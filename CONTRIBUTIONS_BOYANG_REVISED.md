# Contributions Revised

This revised contribution file lists the actual team member names and clarifies the final responsibilities for the project repository, report, and presentation materials.

| Team Member | Primary Role | Detailed Contributions |
|---|---|---|
| Qifan Wang | Data Acquisition & Cleaning | Downloaded and organized the Kaggle Huge Stock Market Dataset; helped validate raw daily price and volume files; supported the cleaning pipeline that removed invalid prices, negative volumes, high-low inconsistencies, insufficient-history assets, low-volume assets, and penny-stock observations; documented key data limitations and filtering decisions used in the final report. |
| Chenyao Qu | Exploratory Analysis & Visualization | Created exploratory summaries for the asset-date panel; analyzed daily return distributions, data coverage, price and volume behavior, and missingness patterns; produced and interpreted the return distribution figure and the momentum quintile visualization; helped explain how aggregate return patterns can hide asset-level differences. |
| Boyang Li | Feature Engineering, Baseline Modeling & GitHub Repository Management | Built the feature engineering workflow for lagged returns, rolling volatility, abnormal volume, liquidity, moving-average distance, drawdown, intraday range, gap return, and market-context features; ensured features used only information available at decision date `t`; implemented baseline modeling with logistic regression; organized the GitHub repository structure, file naming, documentation, and reproducibility materials; integrated code, figures, report files, and presentation assets into the final repository. |
| Jiaheng Xie | Machine Learning & Evaluation | Trained and evaluated the histogram gradient boosting model; compared model performance against logistic regression and baseline strategies; analyzed test-period ROC-AUC, average precision, and feature importance behavior; helped connect classification performance to economic backtest performance and identified limits of model usefulness. |
| Zhiyuan Lin | Presentation Support | Helped prepare presentation materials by reviewing slide flow, formatting selected PowerPoint slides, checking figure placement, and supporting the final presentation revision process. |

All team members contributed to peer feedback and project revision discussions.
