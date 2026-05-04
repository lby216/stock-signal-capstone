# Data Dictionary

## Raw Variables

| Variable | Type | Description |
|---|---:|---|
| `Date` | date | Trading date. |
| `Open` | float | Adjusted opening price. |
| `High` | float | Adjusted highest price during the trading day. |
| `Low` | float | Adjusted lowest price during the trading day. |
| `Close` | float | Adjusted closing price. |
| `Volume` | integer | Number of shares traded. |
| `OpenInt` | integer | Open interest field included in the source files; not used in the main analysis because it is not informative for most equities. |
| `Ticker` | string | Asset symbol derived from the source file name. |
| `AssetType` | string | `Stock`, `ETF`, or `Unknown`, derived from the source folder. |

## Engineered Features

| Variable | Description |
|---|---|
| `ret_1d` | One-day trailing return. |
| `ret_5d` | Five-trading-day trailing return. |
| `ret_21d` | Twenty-one-trading-day trailing return, approximately one month. |
| `ret_63d` | Sixty-three-trading-day trailing return, approximately one quarter. |
| `volatility_5d` | Rolling standard deviation of one-day returns over 5 days. |
| `volatility_21d` | Rolling standard deviation of one-day returns over 21 days. |
| `volatility_63d` | Rolling standard deviation of one-day returns over 63 days. |
| `volume_ratio_21d` | Current volume divided by 21-day average volume. |
| `volume_zscore_63d` | Current volume standardized against the 63-day rolling mean and standard deviation. |
| `dollar_volume_log` | Natural log of one plus `Close * Volume`. |
| `daily_range` | `(High - Low) / Close`, a measure of intraday range. |
| `open_close_return` | `Close / Open - 1`, the intraday open-to-close return. |
| `gap_return` | `Open / previous Close - 1`, the overnight gap return. |
| `price_vs_ma_21d` | `Close / 21-day moving average - 1`. |
| `price_vs_ma_63d` | `Close / 63-day moving average - 1`. |
| `drawdown_63d` | `Close / rolling 63-day maximum Close - 1`. |
| `market_ret_5d` | Market proxy five-day trailing return; SPY if available, otherwise cross-sectional median. |
| `market_volatility_21d` | Market proxy 21-day volatility. |
| `excess_ret_5d` | Asset five-day trailing return minus market proxy five-day return. |

## Target Variables

| Variable | Description |
|---|---|
| `future_ret_5d` | Return from date `t` to `t + 5` trading days. |
| `future_market_ret_5d` | Future five-day return of the market proxy. |
| `future_excess_ret_5d` | Future asset return minus future market return. |
| `future_rank_pct` | Within-date percentile rank of future five-day return. |
| `top_quintile_next_5d` | Binary target equal to 1 if the asset is in the top 20% of future five-day returns on that date. |
| `outperform_market_next_5d` | Binary target equal to 1 if the asset outperforms the market proxy over the next five trading days. |

