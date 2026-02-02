import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Portfolio Tracker", layout="wide")
st.title("Portfolio Tracker")

# Initialize holdings in session state
if "holdings" not in st.session_state:
    st.session_state.holdings = []

# --- Sidebar: Add Holdings ---
with st.sidebar:
    st.header("Add Holding")
    with st.form("add_holding", clear_on_submit=True):
        ticker = st.text_input("Ticker (e.g. AAPL)", "").upper().strip()
        shares = st.number_input("Shares", min_value=0.0, step=1.0, format="%.4f")
        cost_basis = st.number_input("Cost per share ($)", min_value=0.0, step=0.01, format="%.2f")
        submitted = st.form_submit_button("Add")

        if submitted and ticker and shares > 0:
            st.session_state.holdings.append({
                "ticker": ticker,
                "shares": shares,
                "cost_basis": cost_basis,
            })
            st.success(f"Added {shares} shares of {ticker}")

    # Remove holdings
    if st.session_state.holdings:
        st.divider()
        st.subheader("Remove Holding")
        tickers_in_portfolio = [h["ticker"] for h in st.session_state.holdings]
        remove_ticker = st.selectbox("Select ticker to remove", tickers_in_portfolio)
        if st.button("Remove"):
            st.session_state.holdings = [
                h for h in st.session_state.holdings if h["ticker"] != remove_ticker
            ]
            st.rerun()

# --- Main Area: Portfolio Table ---
if not st.session_state.holdings:
    st.info("Add holdings using the sidebar to get started.")
else:
    # Fetch current prices
    tickers = list({h["ticker"] for h in st.session_state.holdings})

    with st.spinner("Fetching prices..."):
        price_data = {}
        for t in tickers:
            try:
                info = yf.Ticker(t)
                fast = info.fast_info
                price_data[t] = fast.last_price
            except Exception:
                price_data[t] = None

    # Build display table
    rows = []
    for h in st.session_state.holdings:
        price = price_data.get(h["ticker"])
        if price is not None:
            market_value = price * h["shares"]
            cost_total = h["cost_basis"] * h["shares"]
            gain_loss = market_value - cost_total
            gain_loss_pct = (gain_loss / cost_total * 100) if cost_total > 0 else 0.0
        else:
            market_value = None
            gain_loss = None
            gain_loss_pct = None

        rows.append({
            "Ticker": h["ticker"],
            "Shares": h["shares"],
            "Cost Basis": h["cost_basis"],
            "Current Price": price,
            "Market Value": market_value,
            "Gain/Loss ($)": gain_loss,
            "Gain/Loss (%)": gain_loss_pct,
        })

    df = pd.DataFrame(rows)

    # Portfolio summary
    total_value = df["Market Value"].sum()
    total_cost = (df["Cost Basis"] * df["Shares"]).sum()
    total_gain = total_value - total_cost if total_value else 0
    total_gain_pct = (total_gain / total_cost * 100) if total_cost > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Portfolio Value", f"${total_value:,.2f}" if total_value else "—")
    col2.metric("Total Gain/Loss", f"${total_gain:,.2f}", f"{total_gain_pct:+.2f}%")
    col3.metric("Positions", len(st.session_state.holdings))

    st.divider()

    # Format the dataframe for display
    st.dataframe(
        df.style.format({
            "Shares": "{:.4f}",
            "Cost Basis": "${:.2f}",
            "Current Price": "${:.2f}",
            "Market Value": "${:,.2f}",
            "Gain/Loss ($)": "${:+,.2f}",
            "Gain/Loss (%)": "{:+.2f}%",
        }),
        use_container_width=True,
        hide_index=True,
    )

    # --- What If: Scenario & Stress Testing ---
    st.divider()
    st.header("What If — Scenario Testing")

    scenario_tab, stress_tab = st.tabs(["Custom Scenario", "Stress Tests"])

    with scenario_tab:
        st.subheader("Uniform Market Move")
        pct_change = st.slider(
            "Simulate a market-wide move (%)",
            min_value=-50, max_value=50, value=0, step=1,
            format="%d%%",
        )

        st.subheader("Per-Ticker Overrides")
        st.caption("Set a custom % change for individual tickers (overrides the uniform move).")
        ticker_overrides = {}
        override_cols = st.columns(min(len(tickers), 4))
        for i, t in enumerate(tickers):
            with override_cols[i % len(override_cols)]:
                val = st.number_input(
                    f"{t} (%)", min_value=-100.0, max_value=200.0,
                    value=float(pct_change), step=1.0, key=f"override_{t}",
                )
                ticker_overrides[t] = val

        # Calculate scenario
        scenario_rows = []
        for h in st.session_state.holdings:
            price = price_data.get(h["ticker"])
            if price is None:
                continue
            move = ticker_overrides.get(h["ticker"], pct_change)
            new_price = price * (1 + move / 100)
            current_val = price * h["shares"]
            new_val = new_price * h["shares"]
            scenario_rows.append({
                "Ticker": h["ticker"],
                "Current Price": price,
                "Scenario Price": new_price,
                "Current Value": current_val,
                "Scenario Value": new_val,
                "Change ($)": new_val - current_val,
            })

        scenario_df = pd.DataFrame(scenario_rows)
        if not scenario_df.empty:
            new_total = scenario_df["Scenario Value"].sum()
            change_total = scenario_df["Change ($)"].sum()
            change_pct = (change_total / total_value * 100) if total_value > 0 else 0

            c1, c2, c3 = st.columns(3)
            c1.metric("Current Value", f"${total_value:,.2f}")
            c2.metric("Scenario Value", f"${new_total:,.2f}")
            c3.metric("Impact", f"${change_total:+,.2f}", f"{change_pct:+.2f}%")

            st.dataframe(
                scenario_df.style.format({
                    "Current Price": "${:.2f}",
                    "Scenario Price": "${:.2f}",
                    "Current Value": "${:,.2f}",
                    "Scenario Value": "${:,.2f}",
                    "Change ($)": "${:+,.2f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

    with stress_tab:
        st.subheader("Historical Stress Scenarios")
        st.caption("See how your portfolio would react under historical market crashes.")

        scenarios = {
            "2008 Financial Crisis": -38.5,
            "COVID Crash (Mar 2020)": -33.9,
            "Dot-com Bust (2000-02)": -49.1,
            "Black Monday (1987)": -22.6,
            "2022 Bear Market": -19.4,
            "Mild Correction (-10%)": -10.0,
        }

        stress_results = []
        for name, drop in scenarios.items():
            scenario_val = total_value * (1 + drop / 100)
            stress_results.append({
                "Scenario": name,
                "Market Drop": f"{drop:+.1f}%",
                "Portfolio Value": scenario_val,
                "Loss ($)": scenario_val - total_value,
            })

        stress_df = pd.DataFrame(stress_results)

        # Bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=stress_df["Scenario"],
            y=stress_df["Portfolio Value"],
            marker_color=["#ef4444"] * len(stress_df),
            text=[f"${v:,.0f}" for v in stress_df["Portfolio Value"]],
            textposition="outside",
        ))
        fig.add_hline(
            y=total_value, line_dash="dash", line_color="#22c55e",
            annotation_text=f"Current: ${total_value:,.0f}",
        )
        fig.update_layout(
            yaxis_title="Portfolio Value ($)",
            xaxis_title="",
            height=400,
            margin=dict(t=30),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            stress_df.style.format({
                "Portfolio Value": "${:,.2f}",
                "Loss ($)": "${:+,.2f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
