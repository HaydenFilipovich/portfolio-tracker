# Portfolio Tracker with AI-Integrated Risk & Stress Testing (OpenAI API Version)

This project is a Streamlit-based portfolio tracker that allows users to track equity holdings in real time, evaluate portfolio risk using advanced quantitative methods, and generate AI-powered risk analysis grounded in live computed metrics.

This branch (`openai`) uses the **OpenAI API with `gpt-4o`** for structured portfolio risk analysis.

---

## Features

### Portfolio Tracking

- Add and remove equity holdings (persisted in SQLite)
- CSV bulk import with template download and validation
- Live price data pulled from Yahoo Finance

**Automatic calculation of:**

- Market value
- Dollar gain/loss
- Percentage return

**Summary metrics:**

- Total portfolio value
- Total gain/loss
- Number of positions

---

### What-If Scenario Testing

- Apply a uniform market-wide price shock (-50% to +50%)
- Override individual ticker returns

---

### Historical Stress Tests

Simulate portfolio performance under major historical market events:

- 2008 Financial Crisis
- COVID Crash (March 2020)
- Dot-com Bust (2000–2002)
- Black Monday (1987)
- 2022 Bear Market

---

## Risk & Performance Analytics

### Performance Metrics

- Annualized return
- Annualized volatility
- Sharpe ratio
- Sortino ratio
- Maximum drawdown

### VaR / CVaR

- Historical VaR & CVaR
- Parametric VaR & CVaR (90/95/99%)
- Correlation-aware parametric VaR

### Monte Carlo Simulation

- Geometric Brownian Motion (GBM)
- Terminal distribution visualization
- Fan charts

---

## AI Risk Brief (OpenAI API)

This branch integrates:

- **Model: `gpt-4o`**
- Deterministic generation (temperature = 0)
- Structured output enforcement

The AI is given live portfolio metrics including:

- Holdings table
- Sharpe & Sortino ratios
- Historical & parametric VaR
- Monte Carlo percentiles
- Stress test results

The response is structured into:

1. Portfolio Overview
2. Key Risk Findings
3. Recommendations

---

## Setup (OpenAI Required)

Install dependencies:

```bash
pip install -r requirements.txt
pip install openai

Create a .env file:

OPENAI_API_KEY=your-key-here

Run the app:

streamlit run app.py

Open in browser:

http://localhost:8502
Architecture
File	Purpose
app.py	Streamlit UI and orchestration
db.py	SQLite persistence
data.py	Market data ingestion
risk.py	Quantitative risk engine
chat.py	OpenAI prompt construction and API integration
Tech Stack

Python

Streamlit

Pandas / NumPy

Plotly

Yahoo Finance (yfinance)

SQLite

OpenAI API (gpt-4o)

Why This Branch Exists

This version demonstrates API-based LLM integration suitable for production-style deployment where external model access is acceptable
