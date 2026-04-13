# Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] - 2026-03-29

### Added
- **Walk-Forward Backtesting** (`walk_forward_backtest_strategy`):
  - Splits data into N folds (train/test) to validate strategy on unseen forward data
  - Per-fold in-sample vs out-of-sample return comparison
  - **Robustness score** (test/train ratio): ROBUST ≥ 0.8 | MODERATE ≥ 0.5 | WEAK ≥ 0.2 | OVERFITTED < 0.2
  - Aggregate out-of-sample metrics: Sharpe, win rate, max drawdown, total return
  - Supports 2–10 splits, configurable train ratio, both 1d and 1h intervals
- **Full Trade Log** (`include_trade_log=True`):
  - Per-trade breakdown: entry/exit date & price, holding days, gross/net return %, cost %
  - Running capital and cumulative return at each trade
- **Equity Curve** (`include_equity_curve=True`):
  - Capital value + drawdown % at each trade exit — ready for charting
- **1h (Hourly) Timeframe** (`interval="1h"`):
  - All strategies and compare now support intraday hourly data
  - Sharpe ratio annualization corrected for 1h bars (252 × 6 trading hours)
  - Works on `backtest_strategy`, `compare_strategies`, and `walk_forward_backtest_strategy`

### Changed
- `backtest_strategy` tool: added `interval`, `include_trade_log`, `include_equity_curve` params
- `compare_strategies` tool: added `interval` param; now documents all 6 strategies (was 4)
- `run_backtest()` now returns last 5 trades always (`recent_trades`) for quick inspection
- Sharpe ratio calculation now uses interval-aware annualization factor

### Notes (personal)
- I changed the default `n_splits` for walk-forward backtesting from 5 to 3 in my local config — found 5 folds too slow on longer date ranges with hourly data.
- Changed default `train_ratio` from 0.7 to 0.8 — I prefer more training data per fold when testing on crypto which tends to be noisier.
- Changed default `interval` from `"1d"` to `"1h"` for `backtest_strategy` — I mostly test short-term setups and hourly is more relevant for my use case.
- Changed default `include_trade_log` from `False` to `True` — I always want the full trade breakdown; easier to just have it on by default than remember to pass the flag each time.
- Changed default `include_equity_curve` from `False` to `True` — same reasoning as trade log; I paste the equity curve into a quick matplotlib script to visualize runs, so having it always available saves a step.
  - Quick snippet I use: `plt.plot([t['capital'] for t in result['equity_curve']]); plt.title('Equity Curve'); plt.show()`
  - Note: requires `matplotlib` installed separately (`pip install matplotlib`) — not a project dependency, just for my local viz workflow.
- Changed default `recent_trades` count from 5 to 10 — 5 trades is often not enough context when reviewing hourly strategies with many short holds; 10 gives a better snapshot.
- Changed default `initial_capital` from 10000 to 1000 — I test with smaller amounts closer to what I actually trade with; makes the output feel more grounded for my use case.
- Changed default `commission` from 0.001 (0.1%) to 0.0025 (0.25%) — better reflects the fees I actually pay on the exchanges I use (Coinbase/Kraken); the original default was too optimistic for retail crypto trading.
