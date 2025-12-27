# Limitations and Scope

## Explicit Statement of Limitations

This research makes empirical claims that are **context-dependent**. This document explicitly states what is and is not claimed.

---

## 1. Turnover-Sharpe Relationship

**What we claim:**
Empirical relationship observed in tested signals: "A 1x increase in annual turnover implies ~X units of Sharpe decay at Y% cost per trade."

**What we do NOT claim:**
- That this coefficient is universal across all signal types
- That it applies to all market conditions
- That it holds for different cost structures
- That it is a law of nature

**Scope:**
- Signal types: Simple technical signals (momentum, mean reversion)
- Market: Liquid equity indices (SPY)
- Time period: 2000-2020
- Cost structure: 0.5% commission + 0.1% spread

**Why this matters:**
The relationship coefficient is **context-dependent**. It should be interpreted as a stylized fact within our study's scope, not generalized beyond tested conditions.

---

## 2. Capacity Estimates

**What we claim:**
Rough capacity estimates based on participation rate × volume, using simplified impact models.

**What we do NOT claim:**
- That these are precise capacity limits
- That the linear impact model is universally accurate
- That participation rates are optimal
- That capacity scales linearly with volume

**Assumptions:**
1. Linear impact model (simplification; actual is sublinear)
2. 1% participation rate (conservative assumption)
3. Constant market conditions (no liquidity crises)
4. Single-asset focus (no portfolio effects)

**Limitations:**
- Impact coefficients vary by asset class
- Market microstructure matters (exchange, time of day)
- Portfolio effects can reduce capacity
- Liquidity crises can collapse capacity

**Why this matters:**
Capacity estimates provide a framework for thinking about scalability, but precise numbers require more sophisticated modeling and may vary significantly with context.

---

## 3. Generalization Claims

**What we claim:**
Empirical thresholds observed in tested signals (e.g., "turnover > X requires costs < Y").

**What we do NOT claim:**
- That these thresholds are universal
- That they apply to all signal types
- That they hold in all market conditions
- That optimization cannot change them

**Scope:**
- Simple technical signals with fixed parameters
- No parameter optimization
- No universe changes
- Tested on liquid equity indices

**Why this matters:**
Thresholds are empirical estimates from our sample. They provide guidance but should not be treated as universal constants. Different signal types, market conditions, or implementation strategies may produce different thresholds.

---

## 4. Cost Models

**What we use:**
Simplified linear models for:
- Commissions (fixed per trade)
- Bid-ask spread (half-spread)
- Slippage (volatility and volume scaled)

**What we do NOT claim:**
- That these models capture all execution complexity
- That slippage is perfectly linear
- That costs don't vary with order size
- That market impact is fully captured

**Simplifications:**
- Linear slippage models (actual may be non-linear)
- Average costs (don't model cost variation)
- No order type optimization
- No execution algorithm sophistication

**Why this matters:**
Our cost models are deliberately simple to avoid overfitting. More sophisticated execution may reduce costs, but our models provide conservative estimates for typical retail/institutional execution.

---

## 5. Statistical vs Economic Edge

**What we claim:**
Clear distinction exists between statistical edge (hit rate > 50%, significant returns) and economic edge (net Sharpe > 0 after costs).

**What we do NOT claim:**
- That all signals follow this pattern
- That optimization cannot bridge the gap
- That costs always eliminate edge
- That our definitions are the only valid ones

**Scope:**
- Binary definitions (edge exists or doesn't)
- Simple cost structure
- No optimization or parameter tuning

**Why this matters:**
The distinction is conceptual and useful for understanding tradability, but the exact definitions and thresholds may vary with context and implementation sophistication.

---

## 6. Time Period and Market Conditions

**What we test:**
Signals on SPY from 2000-2020 (includes multiple market regimes).

**What we do NOT claim:**
- That results apply to all time periods
- That they hold in all market regimes
- That they predict future performance
- That they apply to other asset classes

**Limitations:**
- Single asset (SPY)
- Specific time period (2000-2020)
- Specific market microstructure (US equity markets)
- May not capture regime-specific effects

**Why this matters:**
Results are historical and may not predict future performance. Market structure, technology, and participant behavior change over time.

---

## 7. Signal Definitions

**What we test:**
Simple, well-known signals with fixed parameters (no optimization).

**What we do NOT claim:**
- That these are optimal signal definitions
- That parameter tuning cannot improve results
- That these signals represent all possible strategies
- That optimization cannot rescue untradable signals

**Scope:**
- Fixed parameters (no tuning)
- Simple signal definitions
- No machine learning
- No regime optimization

**Why this matters:**
We test signals as they are commonly defined, not as optimized versions. Optimization may change tradability, but our goal is to understand decay of signals as they exist in practice.

---

## Summary: What This Research Is and Is Not

**This research IS:**
- A tradability study of specific signals in specific conditions
- A demonstration of the distinction between statistical and economic edge
- A critique of naive backtesting without cost modeling
- An empirical investigation of cost-driven decay mechanisms

**This research IS NOT:**
- A universal law of signal decay
- A claim that all signals are untradable
- A statement that optimization cannot help
- A prediction of future performance
- A comprehensive execution analysis

---

## Final Note

All empirical relationships, thresholds, and coefficients in this research are **context-dependent**. They are valid within our study's scope but should not be generalized beyond tested conditions without additional validation.

This is intentional: we aim to provide defensible, transparent analysis with explicit limitations, not universal claims that cannot be defended.

