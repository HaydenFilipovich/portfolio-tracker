import numpy as np
import pandas as pd

from data import TRADING_DAYS

Z_SCORES = {90.0: 1.2816, 95.0: 1.6449, 99.0: 2.3263}
PHI_AT_Z = {90.0: 0.17550, 95.0: 0.10314, 99.0: 0.02665}


def compute_performance(
    port_returns: pd.Series,
    rf_annual: float = 0.05,
    trading_days: int = TRADING_DAYS,
) -> dict:
    """Compute annualized performance metrics from daily portfolio returns."""
    rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1

    mean_daily = port_returns.mean()
    std_daily = port_returns.std()
    ann_return = (1 + mean_daily) ** trading_days - 1
    ann_vol = std_daily * np.sqrt(trading_days)

    sharpe = (ann_return - rf_annual) / ann_vol if ann_vol > 0 else 0.0

    downside = port_returns[port_returns < rf_daily]
    downside_std = downside.std() if len(downside) > 1 else std_daily
    sortino = (
        (ann_return - rf_annual) / (downside_std * np.sqrt(trading_days))
        if downside_std > 0
        else 0.0
    )

    cum_returns = (1 + port_returns).cumprod()
    running_max = cum_returns.cummax()
    drawdown_series = (cum_returns - running_max) / running_max
    max_dd = float(drawdown_series.min())

    return {
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_dd": max_dd,
        "cum_returns": cum_returns,
        "drawdown_series": drawdown_series,
        "mean_daily": mean_daily,
        "std_daily": std_daily,
    }


def compute_var(
    port_returns: pd.Series,
    total_value: float,
    confidence: float = 95.0,
    mean_daily: float | None = None,
    std_daily: float | None = None,
) -> dict:
    """Compute historical and parametric VaR/CVaR."""
    if mean_daily is None:
        mean_daily = port_returns.mean()
    if std_daily is None:
        std_daily = port_returns.std()

    alpha = 1 - confidence / 100
    z = Z_SCORES[confidence]

    # Historical
    hist_q = float(port_returns.quantile(alpha))
    var_hist_pct = -hist_q
    cvar_hist_pct = -float(port_returns[port_returns <= hist_q].mean())
    var_hist_dollar = var_hist_pct * total_value
    cvar_hist_dollar = cvar_hist_pct * total_value

    # Parametric (normal)
    var_param_pct = z * std_daily - mean_daily
    cvar_param_pct = std_daily * PHI_AT_Z[confidence] / alpha - mean_daily
    var_param_dollar = var_param_pct * total_value
    cvar_param_dollar = cvar_param_pct * total_value

    return {
        "var_hist_pct": var_hist_pct,
        "var_hist_dollar": var_hist_dollar,
        "cvar_hist_pct": cvar_hist_pct,
        "cvar_hist_dollar": cvar_hist_dollar,
        "var_param_pct": var_param_pct,
        "var_param_dollar": var_param_dollar,
        "cvar_param_pct": cvar_param_pct,
        "cvar_param_dollar": cvar_param_dollar,
    }


def compute_var_correlation(
    daily_returns: pd.DataFrame,
    weights: pd.Series,
    total_value: float,
    confidence: float = 95.0,
    mean_daily: float | None = None,
) -> dict:
    """Correlation-aware parametric VaR using the variance-covariance matrix.

    Uses: port_vol = sqrt(w' @ Sigma @ w), VaR = z * port_vol - mean_daily.
    This properly accounts for diversification benefits between assets.
    """
    if mean_daily is None:
        mean_daily = daily_returns.dot(weights).mean()

    z = Z_SCORES[confidence]

    # Variance-covariance matrix
    cov_matrix = daily_returns.cov()

    # Align weights to covariance matrix columns
    w = weights.reindex(cov_matrix.columns).fillna(0).values

    # Portfolio volatility: sqrt(w' * Sigma * w)
    port_var = w @ cov_matrix.values @ w
    port_vol = np.sqrt(port_var)

    var_corr_pct = z * port_vol - mean_daily
    var_corr_dollar = var_corr_pct * total_value

    return {
        "var_corr_pct": var_corr_pct,
        "var_corr_dollar": var_corr_dollar,
        "port_vol_daily": port_vol,
    }


def compute_monte_carlo(
    total_value: float,
    mean_daily: float,
    std_daily: float,
    n_sims: int = 5000,
    horizon: int = 21,
) -> dict:
    """Run geometric Brownian Motion Monte Carlo simulation."""
    rng = np.random.default_rng(42)

    rand = rng.standard_normal((n_sims, horizon))
    log_rets = (mean_daily - 0.5 * std_daily**2) + std_daily * rand
    cum_log = np.cumsum(log_rets, axis=1)
    paths = total_value * np.exp(cum_log)

    terminal = paths[:, -1]

    return {
        "paths": paths,
        "terminal": terminal,
        "mc_mean": float(np.mean(terminal)),
        "mc_median": float(np.median(terminal)),
        "mc_5": float(np.percentile(terminal, 5)),
        "mc_95": float(np.percentile(terminal, 95)),
    }
