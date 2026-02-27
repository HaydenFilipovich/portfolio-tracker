def build_system_prompt(
    rows: list[dict],
    totals: dict,
    risk_metrics: dict | None = None,
) -> str:
    """Build the AI chatbot system prompt with portfolio and risk data."""
    lines = [
        "You are a helpful portfolio analysis assistant. You have access to the "
        "user's current portfolio data and risk metrics. Answer questions about "
        "their holdings, performance, and risk clearly and concisely.",
        "",
        "## Current Portfolio",
        f"Total Value: ${totals['total_value']:,.2f}",
        f"Total Cost Basis: ${totals['total_cost']:,.2f}",
        f"Total Gain/Loss: ${totals['total_gain']:+,.2f} ({totals['total_gain_pct']:+.2f}%)",
        f"Positions: {len(rows)}",
        "",
        "### Holdings",
    ]

    for r in rows:
        price_str = f"${r['Current Price']:.2f}" if r["Current Price"] else "N/A"
        val_str = f"${r['Market Value']:,.2f}" if r["Market Value"] else "N/A"
        gl_str = (
            f"${r['Gain/Loss ($)']:+,.2f} ({r['Gain/Loss (%)']:+.2f}%)"
            if r["Gain/Loss ($)"] is not None
            else "N/A"
        )
        lines.append(
            f"- {r['Ticker']}: {r['Shares']:.4f} shares @ ${r['Cost Basis']:.2f} cost | "
            f"Price: {price_str} | Value: {val_str} | G/L: {gl_str}"
        )

    if risk_metrics:
        m = risk_metrics
        lines.extend([
            "",
            "## Risk Metrics (1-year lookback, 95% confidence)",
            f"- Annualized Return: {m['ann_return']:+.2%}",
            f"- Annualized Volatility: {m['ann_vol']:.2%}",
            f"- Sharpe Ratio: {m['sharpe']:.2f}",
            f"- Sortino Ratio: {m['sortino']:.2f}",
            f"- Max Drawdown: {m['max_dd']:.2%}",
            f"- Historical VaR (95%): ${m['var_hist_dollar']:,.0f} ({m['var_hist_pct']:.2%} of portfolio)",
            f"- Historical CVaR (95%): ${m['cvar_hist_dollar']:,.0f} ({m['cvar_hist_pct']:.2%} of portfolio)",
            f"- Correlation-Aware VaR (95%): ${m['var_corr_dollar']:,.0f} ({m['var_corr_pct']:.2%} of portfolio)",
            f"- Monte Carlo 5th/95th percentile (21-day): ${m['mc_5']:,.0f} / ${m['mc_95']:,.0f}",
        ])

    return "\n".join(lines)
