# Who Is Wrong Because of This Result?

## Explicit Critique Section

This research invalidates specific beliefs held by identifiable groups. This section names them.

---

### 1. Retail Quants Who Believe Hit Rate Implies Profitability

**What they believe:**
> "If my signal has hit rate > 50%, it's profitable."

**Why they're wrong:**
Our results show hit rates of 50.7% (momentum) and similar (mean reversion) **survive costs**, yet both signals become unprofitable after transaction costs. Directional correctness ≠ profitability.

**Evidence:**
- Momentum: 50.7% hit rate → -0.10% annualized return after costs
- Mean reversion: Hit rate persists → Net Sharpe collapses to negative
- Hit rate survival: 99.7% (direction correct)
- PnL collapse: -104.9% (returns turn negative)

**Who needs to read this:**
- Individual traders optimizing for "win rate"
- Quant bloggers publishing "backtests" with >50% hit rates
- Reddit r/algotrading posts claiming profitability based on hit rate alone

---

### 2. Academic Papers That Ignore Implementability

**What they do:**
> Publish signals with Sharpe > 1.0, hit rate > 55%, but never model transaction costs or capacity constraints.

**Why they're wrong:**
Our results show signals can have statistical edge (Sharpe > 0, hit rate > 50%) but **zero economic edge** when costs are included. Academic backtests without cost modeling are incomplete.

**Evidence:**
- Gross Sharpe: 0.102 (momentum), 0.542 (mean reversion) → Looks publishable
- Net Sharpe: -0.005 (momentum), negative (mean reversion) → Actually untradable
- Break-even costs: 0.672% and 0.082% per trade → Below realistic retail/institutional costs

**Who needs to read this:**
- Authors of factor research papers (Fama-French style) that don't model costs
- Journal editors accepting papers without implementability analysis
- PhD students writing dissertations on "profitable signals" without cost modeling

**Specific failure mode:**
Papers published in top journals with gross Sharpe > 1.0 that become unprofitable at 0.5% transaction costs (realistic retail level).

---

### 3. Backtests That Implicitly Assume Zero Friction

**What they assume:**
> Perfect execution, no slippage, infinite capacity, zero bid-ask spread.

**Why they're wrong:**
Our cost analysis shows:
- 2.10% annualized cost drag (momentum signal)
- 0.672% break-even cost per trade
- Mean reversion breaks even at 0.082% per trade (effectively untradable)

These assumptions are not conservative; they're **fundamentally wrong** for most signal types.

**Evidence:**
- Cost drag exceeds gross return: 2.10% drag vs 2.00% gross return
- Signals with turnover > 3x/year require costs < 0.7% per trade
- Realistic retail costs (0.5% commission + 0.1% spread) = 0.6% per trade → Eliminates edge

**Who needs to read this:**
- Quantitative hedge funds running backtests without cost models
- Systematic traders using Zipline/Backtrader with default cost assumptions
- Academic researchers using CRSP/Compustat data without modeling execution

**Specific failure mode:**
Backtests showing 15% annual returns that disappear when realistic costs (0.5-1% per trade) are included.

---

### 4. Systematic Traders Who Optimize for Gross Sharpe

**What they do:**
> Select signals based on gross Sharpe ratio, assuming net Sharpe ≈ gross Sharpe.

**Why they're wrong:**
Our results show gross-to-net Sharpe decay of **-104.9%** (momentum signal). Gross Sharpe is not a reliable proxy for tradability.

**Evidence:**
- Gross Sharpe: 0.102 → Net Sharpe: -0.005 (momentum)
- Gross Sharpe: 0.542 → Net Sharpe: negative (mean reversion at 0.2% costs)
- Turnover is the mechanism: 3.0x annual turnover → 2.10% cost drag

**Who needs to read this:**
- Quant PMs selecting signals from research papers
- Systematic funds constructing factor portfolios
- Algorithmic traders screening for "high Sharpe" strategies

**Specific failure mode:**
Portfolio optimization based on gross Sharpe that produces net-negative portfolios after implementation.

---

### 5. The "All Alpha Decays" Overgeneralization

**What some believe:**
> "All signals decay after discovery, so nothing works."

**Why this overcorrects:**
Our results show **statistical edge persists** (hit rates remain >50%) but **economic edge disappears** (costs overwhelm residual alpha). The failure is not signal falsification—it's implementation failure.

**Evidence:**
- Hit rate survival: 99.7% (momentum), similar (mean reversion)
- Statistical edge: Still present (hit rate > 50%)
- Economic edge: Eliminated (net Sharpe < 0)

**Who needs to read this:**
- Skeptics who dismiss all quant research as "overfitted"
- Academics who argue markets are perfectly efficient
- Practitioners who believe "if it worked, it would be gone"

**Correct interpretation:**
Signals don't disappear; they become **uneconomical to trade**. The bottleneck is not information efficiency—it's **implementation frictions**.

---

## The Real Claim (Who Should Change Behavior)

**Primary audience:** Quantitative researchers who publish backtests without cost modeling.

**Secondary audience:** Systematic traders who select signals based on gross performance metrics.

**Tertiary audience:** Academic journals that accept factor research without implementability analysis.

**The change required:**
1. **Always report break-even cost** alongside gross Sharpe
2. **Model turnover explicitly** as a first-class variable
3. **Separate statistical edge from economic edge** in reporting
4. **Report net Sharpe, not just gross Sharpe**

---

## What This Result Does NOT Claim

- ❌ That all signals are untradable
- ❌ That costs always eliminate alpha
- ❌ That backtests are useless
- ❌ That markets are perfectly efficient

**What it DOES claim:**
- ✅ Signals can have statistical edge without economic edge
- ✅ Turnover is the primary mechanism for cost-driven failure
- ✅ Hit rate persistence does not imply profitability
- ✅ Gross performance metrics are misleading without cost modeling

---

## Bottom Line

If you publish a backtest showing Sharpe > 0.5 without reporting break-even transaction costs, **you are part of the problem this research identifies**.

