"""
Tradability Analysis Module

Main integration module for economic decay analysis.
Computes gross vs net performance, break-even costs, and economic viability.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Tuple
from datetime import datetime

from decay_analysis import compute_performance_metrics, PerformanceMetrics
from transaction_costs import (
    compute_total_explicit_costs,
    compute_net_returns_from_positions,
    compute_annual_turnover
)
from slippage import (
    compute_total_slippage,
    compute_net_returns_with_slippage
)
from capacity import estimate_maximum_viable_capital


class TradabilityMetrics:
    """Container for tradability metrics."""
    
    def __init__(self):
        self.gross_metrics: Optional[PerformanceMetrics] = None
        self.net_metrics: Optional[PerformanceMetrics] = None
        self.break_even_cost: Optional[float] = None
        self.annual_turnover: Optional[float] = None
        self.cost_drag: Optional[float] = None
        self.max_viable_capacity: Optional[float] = None
        self.hit_rate_survival: Optional[float] = None  # Hit rate before/after costs
        self.pnl_collapse: Optional[float] = None  # PnL before/after costs
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for easy export."""
        return {
            'gross_sharpe': self.gross_metrics.sharpe_ratio if self.gross_metrics else None,
            'net_sharpe': self.net_metrics.sharpe_ratio if self.net_metrics else None,
            'gross_return': self.gross_metrics.return_mean if self.gross_metrics else None,
            'net_return': self.net_metrics.return_mean if self.net_metrics else None,
            'break_even_cost': self.break_even_cost,
            'annual_turnover': self.annual_turnover,
            'cost_drag': self.cost_drag,
            'max_viable_capacity': self.max_viable_capacity,
            'hit_rate_survival': self.hit_rate_survival,
            'pnl_collapse': self.pnl_collapse,
        }


def compute_positions_from_returns(returns: pd.Series, 
                                   signals: pd.Series,
                                   quantile: float = 0.5) -> pd.Series:
    """
    Reconstruct positions from signals (used for cost computation).
    
    Args:
        returns: Strategy returns series (for alignment)
        signals: Signal values series
        quantile: Threshold for long/short positions
    
    Returns:
        Series of positions (-1, 0, 1)
    """
    # Align signals with returns
    aligned_signals = signals.reindex(returns.index, method='ffill')
    
    # Compute threshold
    signal_threshold = aligned_signals.quantile(quantile)
    
    # Binary positions: 1 if above threshold, -1 if below
    positions = np.where(aligned_signals > signal_threshold, 1, -1)
    
    return pd.Series(positions, index=returns.index)


def compute_gross_vs_net_performance(gross_returns: pd.Series,
                                     positions: pd.Series,
                                     commission_per_trade: float = 0.005,
                                     half_spread: float = 0.001,
                                     volatility: Optional[pd.Series] = None,
                                     volumes: Optional[pd.Series] = None,
                                     prices: Optional[pd.Series] = None,
                                     vol_impact_coefficient: float = 0.1,
                                     vol_impact_coefficient2: float = 0.0001,
                                     periods_per_year: int = 252) -> TradabilityMetrics:
    """
    Compute gross vs net performance after all costs.
    
    Args:
        gross_returns: Gross strategy returns (before costs)
        positions: Series of position values
        commission_per_trade: Commission cost per trade
        half_spread: Half of bid-ask spread
        volatility: Optional volatility series
        volumes: Optional volume series
        prices: Optional price series
        vol_impact_coefficient: Volatility impact coefficient
        vol_impact_coefficient2: Volume impact coefficient
        periods_per_year: Number of periods per year
    
    Returns:
        TradabilityMetrics object with gross and net performance
    """
    metrics = TradabilityMetrics()
    
    # Compute gross metrics
    metrics.gross_metrics = compute_performance_metrics(gross_returns)
    
    # Compute explicit costs
    explicit_costs = compute_total_explicit_costs(
        positions, commission_per_trade, half_spread, prices, periods_per_year
    )
    explicit_costs_aligned = explicit_costs.reindex(gross_returns.index, method='ffill').fillna(0)
    
    # Compute slippage
    slippage = compute_total_slippage(
        positions, volatility, volumes, prices,
        vol_impact_coefficient, vol_impact_coefficient2,
        periods_per_year
    )
    slippage_aligned = slippage.reindex(gross_returns.index, method='ffill').fillna(0)
    
    # Total costs
    total_costs = explicit_costs_aligned + slippage_aligned
    
    # Net returns
    net_returns = gross_returns - total_costs
    
    # Compute net metrics
    metrics.net_metrics = compute_performance_metrics(net_returns)
    
    # Annual turnover
    metrics.annual_turnover = compute_annual_turnover(positions, periods_per_year)
    
    # Cost drag (average cost per period, annualized)
    avg_cost_per_period = total_costs.mean()
    metrics.cost_drag = avg_cost_per_period * periods_per_year
    
    # Hit rate survival (hit rate before vs after)
    if metrics.gross_metrics.hit_rate is not None and metrics.net_metrics.hit_rate is not None:
        metrics.hit_rate_survival = metrics.net_metrics.hit_rate / metrics.gross_metrics.hit_rate
    
    # PnL collapse (return before vs after)
    if metrics.gross_metrics.return_mean is not None and metrics.net_metrics.return_mean is not None:
        if abs(metrics.gross_metrics.return_mean) > 1e-6:
            metrics.pnl_collapse = metrics.net_metrics.return_mean / metrics.gross_metrics.return_mean
    
    return metrics


def compute_break_even_cost(gross_returns: pd.Series,
                            positions: pd.Series,
                            periods_per_year: int = 252,
                            tolerance: float = 1e-6) -> float:
    """
    Compute break-even transaction cost (cost level where net Sharpe ≈ 0).
    
    Args:
        gross_returns: Gross strategy returns
        positions: Series of position values
        periods_per_year: Number of periods per year
        tolerance: Tolerance for break-even (default 1e-6)
    
    Returns:
        Break-even cost per trade (as fraction)
    """
    # Binary search for break-even cost
    low_cost = 0.0
    high_cost = 0.1  # 10% per trade (very high upper bound)
    
    for _ in range(50):  # Max 50 iterations
        mid_cost = (low_cost + high_cost) / 2.0
        
        # Compute net returns at this cost level
        net_returns = compute_net_returns_from_positions(
            gross_returns, positions,
            commission_per_trade=mid_cost,
            half_spread=0.0,  # Only test commission for simplicity
            periods_per_year=periods_per_year
        )
        
        # Compute Sharpe ratio
        net_metrics = compute_performance_metrics(net_returns)
        
        if net_metrics.sharpe_ratio is None:
            sharpe = 0.0
        else:
            sharpe = net_metrics.sharpe_ratio
        
        # Check if break-even (Sharpe ≈ 0)
        if abs(sharpe) < tolerance:
            return mid_cost
        
        if sharpe > 0:
            # Still profitable, try higher cost
            low_cost = mid_cost
        else:
            # Unprofitable, try lower cost
            high_cost = mid_cost
    
    # Return midpoint as approximation
    return (low_cost + high_cost) / 2.0


def analyze_tradability(gross_returns: pd.Series,
                        signals: pd.Series,
                        positions: Optional[pd.Series] = None,
                        commission_per_trade: float = 0.005,
                        half_spread: float = 0.001,
                        volatility: Optional[pd.Series] = None,
                        volumes: Optional[pd.Series] = None,
                        prices: Optional[pd.Series] = None,
                        vol_impact_coefficient: float = 0.1,
                        vol_impact_coefficient2: float = 0.0001,
                        periods_per_year: int = 252,
                        sharpe_threshold: float = 0.5) -> TradabilityMetrics:
    """
    Comprehensive tradability analysis.
    
    Args:
        gross_returns: Gross strategy returns
        signals: Signal values (for position reconstruction if needed)
        positions: Optional pre-computed positions (if None, reconstructed from signals)
        commission_per_trade: Commission cost per trade
        half_spread: Half of bid-ask spread
        volatility: Optional volatility series
        volumes: Optional volume series
        prices: Optional price series
        vol_impact_coefficient: Volatility impact coefficient
        vol_impact_coefficient2: Volume impact coefficient
        periods_per_year: Number of periods per year
        sharpe_threshold: Sharpe threshold for capacity analysis
    
    Returns:
        TradabilityMetrics object with all metrics
    """
    # Reconstruct positions if not provided
    if positions is None:
        positions = compute_positions_from_returns(gross_returns, signals)
    
    # Compute gross vs net performance
    metrics = compute_gross_vs_net_performance(
        gross_returns, positions,
        commission_per_trade, half_spread,
        volatility, volumes, prices,
        vol_impact_coefficient, vol_impact_coefficient2,
        periods_per_year
    )
    
    # Break-even cost
    metrics.break_even_cost = compute_break_even_cost(
        gross_returns, positions, periods_per_year
    )
    
    # Capacity analysis
    if volumes is not None:
        capacity_result = estimate_maximum_viable_capital(
            gross_returns, positions, volumes, prices,
            sharpe_threshold=sharpe_threshold,
            periods_per_year=periods_per_year
        )
        metrics.max_viable_capacity = capacity_result['max_viable_capacity']
    
    return metrics


def compute_drawdown_sensitivity_to_costs(gross_returns: pd.Series,
                                          positions: pd.Series,
                                          cost_levels: Optional[np.ndarray] = None,
                                          periods_per_year: int = 252) -> pd.DataFrame:
    """
    Compute drawdown sensitivity as function of transaction costs.
    
    Args:
        gross_returns: Gross strategy returns
        positions: Series of position values
        cost_levels: Array of cost levels to test (default: 0 to 1%)
        periods_per_year: Number of periods per year
    
    Returns:
        DataFrame with columns: cost_level, max_drawdown, sharpe_ratio
    """
    if cost_levels is None:
        cost_levels = np.linspace(0, 0.01, 50)  # 0 to 1%
    
    results = []
    
    for cost in cost_levels:
        # Compute net returns at this cost level
        net_returns = compute_net_returns_from_positions(
            gross_returns, positions,
            commission_per_trade=cost,
            half_spread=0.0,
            periods_per_year=periods_per_year
        )
        
        # Compute metrics
        metrics = compute_performance_metrics(net_returns)
        
        results.append({
            'cost_level': cost,
            'max_drawdown': metrics.max_drawdown,
            'sharpe_ratio': metrics.sharpe_ratio,
            'return_mean': metrics.return_mean,
        })
    
    return pd.DataFrame(results)

