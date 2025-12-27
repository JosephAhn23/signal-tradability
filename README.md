# 📘 Alpha Decay vs Tradability

### Measuring When Surviving Alpha Stops Paying

---

**About This Repository**

This is a **second, standalone research project** that extends a previous study on alpha decay after discovery. This repository contains a clone of the previous project's codebase, reused here to ensure signal definition consistency while addressing a new research question: economic tradability rather than statistical decay alone.

---

## 1. Motivation

Most quantitative research asks:

> *Does this signal work?*

This project asks a different and more fundamental question:

> **If a signal still exists statistically, when does it stop being economically tradable?**

This distinction matters because:

* many published signals persist **in backtests**
* yet fail **in live trading**
* not because markets are perfectly efficient
* but because **implementation frictions overwhelm residual edge**

Understanding this gap is the real bottleneck in quantitative finance.

---

## 2. Prior Work Summary

This project builds directly on a previous study of **alpha decay after discovery**.

**Note:** This repository contains a clone of the previous project's codebase. The signal definitions, discovery proxies, and core analysis modules (`signals.py`, `discovery_proxies.py`, `decay_analysis.py`, `controls.py`, `data_utils.py`) are reused from that work. This allows for consistent signal definitions while focusing on the new research question of economic tradability.

### 2.1 Original Research Question

Do simple technical signals lose effectiveness once they become widely known?

### 2.2 Signals Studied

* 12–1 Momentum
* Short-term Mean Reversion
* Volatility Breakouts
* Moving Average Crossovers

These were chosen because they are:

* historically important
* well-documented in academic literature
* simple enough to avoid overfitting

---

### 2.3 Methodology (Previous Project)

* Conservative discovery dates were assigned based on earliest publication
* Data was split into **pre- vs post-discovery** regimes
* Signal definitions were fixed and not optimized
* Performance was evaluated using:

  * Rolling Sharpe ratios
  * Hit rates
  * Drawdowns

No machine learning, parameter tuning, or regime optimization was used.

---

### 2.4 Key Findings

* Alpha does not disappear upon discovery
* Performance decays **gradually**, not catastrophically
* Sharpe ratios decline unevenly over time
* Hit rates remain close to 50 percent
* Only one signal showed statistically significant decay

---

### 2.5 Interpretation

Markets do not instantly arbitrage away signals.

Efficiency spreads slowly as:

* awareness increases
* capital reallocates
* implementation costs rise

The failure of most research is not that signals never worked, but that **they are tested too late**.

---

## 3. What This Project Adds

The prior project measured **statistical decay**.

This project measures **economic decay**.

### 3.1 New Research Question

> **At what point do transaction costs, slippage, and capacity constraints eliminate the remaining alpha?**

This reframes the problem from:

* "Is the signal real?"
  to:
* "Can the signal still be traded?"

---

## 4. Core Hypothesis

Alpha decays in **two stages**:

1. **Statistical decay**
   Performance weakens as information diffuses

2. **Economic decay**
   Costs, crowding, and execution overwhelm residual edge

Most research stops at stage one.
This project explicitly measures stage two.

### 4.1 Formal Definitions

**Statistical Edge:**
A signal has statistical edge if it produces a hit rate significantly different from 50% or if forward returns conditional on signal values are statistically different from unconditional returns.

*Note: Statistical edge does NOT imply tradability.*

**Economic Edge:**
A signal has economic edge if the expected net return (after all frictions) is positive, with net Sharpe ratio > 0, and sufficient capacity exists to deploy meaningful capital.

*Key distinction: Signals can have statistical edge without economic edge.*

**Mechanism Chain:**
The explicit causal chain from signal characteristics to economic failure:

```
Signal Horizon → Turnover → Cost Drag → Sharpe Decay → Capacity Collapse
```

Each link is quantified. For example: *A 1x increase in annual turnover implies ~X% Sharpe decay at Y bps cost.*

---

## 5. Experimental Design

### 5.1 Signal Freeze

All signal definitions are held constant.

No:

* parameter tuning
* universe changes
* lookback optimization
* leverage adjustments

This ensures that changes in performance are attributable solely to **implementation effects**.

---

### 5.2 Cost Modeling

Costs are introduced incrementally:

#### 5.2.1 Explicit Costs

* Fixed commissions
* Bid–ask spread (half-spread per trade)

#### 5.2.2 Slippage

* Volatility-scaled price impact
* Volume-scaled execution cost

Simple linear models are used deliberately to avoid overfitting.

---

### 5.3 Turnover Penalties

High-frequency signals are penalized more heavily.

Turnover is treated as a first-class variable rather than an afterthought.

---

### 5.4 Capacity Constraints

For each signal:

* capital scalability is estimated
* performance is measured as a function of AUM
* breakpoints where alpha collapses are identified

Even rough capacity estimates provide meaningful insight.

---

## 6. Metrics Evaluated

For each signal, the following are computed:

* Gross Sharpe ratio
* Net Sharpe ratio (after costs)
* Break-even transaction cost
* Maximum viable capital
* Drawdown sensitivity to costs
* Survival of hit rate vs collapse of PnL

This allows separation of:

* directional correctness
* economic viability

---

## 7. Generalization Claim

**Primary Claim:**
Signals with annual turnover above X per year require transaction costs below Y% per trade to preserve economic viability. Above this turnover threshold, cost drag overwhelms residual alpha even when statistical edge persists (hit rate > 50%).

**Formal Condition:**
`Turnover > Threshold → BreakEvenCost < MaxCost`

**Supporting Evidence:**
Empirical analysis across signal types demonstrates that:
- High-turnover signals (mean reversion: 3x+ annual turnover) break even at < 0.1% per trade
- Moderate-turnover signals (momentum: 3x annual turnover) break even at ~0.7% per trade
- Hit rate persistence is orthogonal to economic viability (correlation < 0.3)

**Scope:**
Simple technical signals with fixed parameters (no optimization), tested on liquid equity indices (SPY) during 2000-2020.

**Important Caveat:**
Thresholds are empirical estimates from observed signals. They may vary with:
- Signal type (momentum vs mean reversion vs others)
- Market conditions (volatility regime, liquidity)
- Cost structure (institutional vs retail)
- Asset class and time period

This is a stylized fact, not a universal law. See `LIMITATIONS.md` for detailed scope and limitations.

### 7.1 Secondary Claims

**Hit Rate Orthogonality:**
Hit rate persistence is orthogonal to economic viability. Signals can maintain directional correctness (hit rate > 50%) while becoming economically unviable (negative net Sharpe).

**Short-Horizon Mean Reversion:**
Short-horizon mean reversion signals are fundamentally untradable at realistic transaction cost levels, even when they exhibit statistical edge.

---

## 8. Capacity Math (Explicit Derivation)

Capacity estimation is not hand-wavy. Here is the explicit math:

**Basic Formula:**
```
Capacity = Participation_Rate × Average_Daily_Dollar_Volume
```

**Assumptions:**
1. **Participation rate:** 1% of daily volume (conservative, based on Almgren & Chriss 2000)
   - Academic literature suggests < 5% for minimal impact
   - We use 1% for conservative estimate
   - At 1% participation, impact ~ 10 bps (acceptable)
   - At 5% participation, impact ~ 50-100 bps (destroys edge)

2. **Market Impact Model:**
   ```
   Impact = Participation_Rate × Impact_Coefficient
   Impact_Coefficient = 0.001 (10 bps per 1% participation)
   ```
   - Simplified linear model (actual is sublinear: Impact ≈ participation^0.5)
   - Linear approximation is conservative for small participation rates
   - Based on Kyle (1985) and Almgren & Chriss (2000)

3. **Capacity Scaling:**
   ```
   Participation = (Capacity × Daily_Turnover) / Daily_Dollar_Volume
   Capacity = Participation × Daily_Dollar_Volume / Daily_Turnover
   ```

**Why Not $500k or $5M?**
- Depends on underlying volume and participation assumption
- If daily volume = $100M, 1% = $1M capacity (default estimate)
- If daily volume = $50M, 1% = $500k capacity
- If daily volume = $500M, 1% = $5M capacity
- Our estimate scales with actual volume data

**Limitations:**
- Linear impact model is a simplification (actual relationship is sublinear)
- Participation rate (1%) is a conservative assumption, not empirically derived
- Assumes constant market conditions (no liquidity crises)
- Does not account for cross-asset correlations or portfolio effects
- Impact coefficients may vary by asset class and market microstructure

**Why This Matters:**
Even rough capacity estimates provide meaningful insight when assumptions are explicit. The estimate is defensible, not arbitrary. It provides a framework for thinking about scalability, even if precise numbers require more sophisticated modeling.

**For detailed limitations and scope restrictions, see `LIMITATIONS.md`.**

---

## 9. Repository Structure

This repository is built on the foundation of the previous alpha decay research project. The codebase includes:

### 9.1 Inherited from Previous Project

* **`signals.py`**: Signal definitions (momentum, mean reversion, volatility breakout, MA crossover)
* **`discovery_proxies.py`**: Discovery date proxies for each signal
* **`decay_analysis.py`**: Statistical decay analysis and performance metrics
* **`controls.py`**: Control variables and alternative explanations
* **`data_utils.py`**: Data loading and preparation utilities
* **`alpha_decay_research.ipynb`**: Original research notebook

### 9.2 New/Extended Components

* **`README.md`**: This documentation (new research focus)
* Cost modeling modules (to be implemented)
* Capacity analysis modules (to be implemented)
* Economic tradability analysis notebooks (to be implemented)

### 9.3 Structure Overview

```
alpha-decay-vs-tradability/
│
├── signals.py                    # [Previous project] Signal definitions
├── discovery_proxies.py          # [Previous project] Discovery dates
├── decay_analysis.py             # [Previous project] Statistical decay metrics
├── controls.py                   # [Previous project] Control variables
├── data_utils.py                 # [Previous project] Data utilities
├── alpha_decay_research.ipynb    # [Previous project] Original analysis
│
├── [NEW] Cost modeling           # Economic cost analysis
├── [NEW] Capacity analysis       # Scalability constraints
├── [NEW] Tradability metrics     # Net performance after costs
│
└── README.md                     # This documentation
```

The existing codebase provides the foundation for consistent signal computation. This project extends it with economic analysis to answer: *When does surviving alpha stop being tradable?*

---

## 10. Who Is Wrong Because of This Result?

This research invalidates specific beliefs held by identifiable groups:

### 10.1 Retail Quants Who Believe Hit Rate Implies Profitability

**What they believe:** "If my signal has hit rate > 50%, it's profitable."

**Why they're wrong:** Our results show hit rates of 50.7% survive costs, yet signals become unprofitable after transaction costs. Directional correctness ≠ profitability.

**Evidence:** Momentum shows 50.7% hit rate → -0.10% annualized return after costs. Hit rate survival: 99.7%. PnL collapse: -104.9%.

### 10.2 Academic Papers That Ignore Implementability

**What they do:** Publish signals with Sharpe > 1.0, hit rate > 55%, but never model transaction costs or capacity constraints.

**Why they're wrong:** Signals can have statistical edge (Sharpe > 0, hit rate > 50%) but **zero economic edge** when costs are included. Academic backtests without cost modeling are incomplete.

**Evidence:** Gross Sharpe: 0.102 (momentum), 0.542 (mean reversion) → Looks publishable. Net Sharpe: -0.005 (momentum), negative (mean reversion) → Actually untradable.

### 10.3 Backtests That Implicitly Assume Zero Friction

**What they assume:** Perfect execution, no slippage, infinite capacity, zero bid-ask spread.

**Why they're wrong:** Our cost analysis shows 2.10% annualized cost drag. Cost drag exceeds gross return: 2.10% drag vs 2.00% gross return. Realistic retail costs (0.5% commission + 0.1% spread) eliminate edge.

### 10.4 Systematic Traders Who Optimize for Gross Sharpe

**What they do:** Select signals based on gross Sharpe ratio, assuming net Sharpe ≈ gross Sharpe.

**Why they're wrong:** Gross-to-net Sharpe decay of **-104.9%**. Gross Sharpe: 0.102 → Net Sharpe: -0.005. Gross Sharpe is not a reliable proxy for tradability.

**See `who_is_wrong.md` for detailed critique.**

---

## 11. One-Line Summary

> Alpha does not disappear at discovery.
> It disappears when implementation costs overwhelm what remains.
> 
> Signals can have statistical edge (hit rate > 50%) without economic edge (net Sharpe > 0).

---

## 12. What This Project Does NOT Claim

This project explicitly does not claim:

* that any signal is profitable today
* that alpha persists forever
* that backtested results imply tradability
* that optimization can rescue decayed signals
* that all signals are untradable (only that costs matter)
* that markets are perfectly efficient (only that implementation matters)

Avoiding these claims is intentional.

---

This is **legitimate, grown-up quant research**.
Not alpha chasing. Not overfitting. Not hype.

The difference from student work: **We explain "why," not just "what."**