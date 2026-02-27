import streamlit as st
import yfinance as yf
import pandas as pd

TRADING_DAYS = 252

LOOKBACK_MAP = {"6 Months": 183, "1 Year": 365, "2 Years": 730}

STRESS_SCENARIOS = {
    "2008 Financial Crisis": ("2007-10-01", "2009-03-31"),
    "COVID Crash (Mar 2020)": ("2020-02-01", "2020-04-30"),
    "Dot-com Bust (2000-02)": ("2000-03-01", "2002-10-31"),
    "Black Monday (1987)":    ("1987-09-01", "1987-12-31"),
    "2022 Bear Market":       ("2022-01-01", "2022-10-31"),
}


@st.cache_data(ttl=300, show_spinner=False)
def get_current_price(ticker: str) -> float | None:
    """Return the last price for a ticker, or None on failure."""
    try:
        return yf.Ticker(ticker).fast_info.last_price
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def download_prices(ticker: str, start: str, end: str) -> pd.Series:
    """Download adjusted close prices for a ticker in a date range."""
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if df.empty:
        return pd.Series(dtype=float)
    return df["Close"].squeeze()


def peak_to_trough(prices: pd.Series) -> float:
    """Return the max drawdown (negative float) from a price series."""
    if prices.empty or len(prices) < 2:
        return 0.0
    cummax = prices.cummax()
    drawdown = (prices - cummax) / cummax
    return float(drawdown.min())
