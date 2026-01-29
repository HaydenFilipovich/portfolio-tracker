import streamlit as st
import yfinance as yf
import pandas as pd

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
