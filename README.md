Alpha Decay vs Tradability
Measuring When Surviving Alpha Stops Paying

ABOUT THIS REPOSITORY

This is a standalone research project that extends prior work on alpha decay after discovery. The project reuses the earlier codebase to preserve consistent signal definitions while focusing on a new question: economic tradability rather than statistical decay alone.

MOTIVATION

Most quantitative research asks whether a signal works.

This project asks a more fundamental question. If a signal still exists statistically, when does it stop being economically tradable?

Many published signals continue to appear profitable in backtests but fail in live trading. This is not necessarily because markets are perfectly efficient, but because implementation frictions overwhelm the remaining edge. Understanding this gap is a core problem in quantitative finance.

PRIOR WORK SUMMARY

This project builds directly on prior research studying alpha decay after discovery. The same signal definitions, discovery proxies, and core analysis methods are reused to ensure consistency.

The signals studied include momentum, short-term mean reversion, volatility breakouts, and moving average crossovers. These signals are historically important, well documented in academic literature, and simple enough to avoid overfitting.

The earlier work showed that alpha does not disappear at discovery. Performance decays gradually rather than catastrophically. Hit rates often remain near fifty percent even as Sharpe ratios decline. Statistical edge can persist long after publication.

WHAT THIS PROJECT ADDS

The prior work measured statistical decay. This project measures economic decay.

The central question is when transaction costs, slippage, and capacity constraints eliminate the remaining alpha. The focus shifts from whether a signal is real to whether it can still be traded.

CORE HYPOTHESIS

Alpha decays in two stages.

First, statistical decay occurs as information diffuses and competition increases.

Second, economic decay occurs when costs, crowding, and execution overwhelm the remaining edge.

Most research stops at the first stage. This project explicitly measures the second stage.

A key distinction is that statistical edge does not imply economic edge. Signals may retain hit rates above fifty percent while producing negative net returns after costs.

METHODOLOGY

Signal definitions are frozen. No parameter tuning, optimization, or regime selection is used.

Transaction costs are introduced incrementally through commissions, bid-ask spread, and slippage scaled by volatility and volume. Turnover is treated as a primary driver of cost drag. Capacity is estimated using conservative participation assumptions.

Performance is evaluated using gross versus net Sharpe ratios, break-even transaction costs, capacity thresholds, drawdown sensitivity to costs, and the divergence between hit rate persistence and PnL collapse.

KEY FINDINGS

High-turnover signals lose economic viability quickly even when statistical edge persists. Hit rate persistence is largely orthogonal to profitability. Short-horizon mean reversion is untradable under realistic cost assumptions. Gross Sharpe is a poor proxy for tradability.

GENERALIZATION

Signals with sufficiently high turnover require unrealistically low transaction costs to remain economically viable. Above a turnover threshold, cost drag overwhelms residual alpha even when statistical edge persists.

These results are observed across multiple simple technical signals using fixed parameters on liquid equity index data. Thresholds depend on market conditions, cost structure, and asset class and should be interpreted as empirical, not universal.

CAPACITY MODEL

Capacity is estimated as a function of participation rate and average daily dollar volume using conservative assumptions. While simplified, the model is explicit and defensible and provides meaningful insight into scalability limits.

SUMMARY

Alpha rarely disappears at discovery. It disappears when implementation costs overwhelm what remains.
