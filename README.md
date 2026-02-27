# Portfolio Tracker with AI-Integrated Risk & Stress Testing (Local LLM Version)

This project is a Streamlit-based portfolio tracker that allows users to track equity holdings in real time, evaluate portfolio risk using advanced quantitative methods, and generate AI-powered risk analysis grounded in live computed metrics.

This branch (`main`) uses **Ollama with a locally hosted LLM (`llama3.2`)**, enabling fully offline, cost-free AI integration.

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

**Compare:**

- Current portfolio value
- Scenario portfolio value
- Dollar and percentage impact

---

### Historical Stress Tests

Simulate portfolio performance under major historical market events using actual per-ticker peak-to-trough drawdowns:

- 2008 Financial Crisis
- COVID Crash (March 2020)
- Dot-com Bust (2000–2002)
- Black Monday (1987)
- 2022 Bear Market

Per-ticker breakdown available in expandable panels.

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
- Parametric (normal) VaR & CVaR at 90/95/99% confidence
- Correlation-aware parametric VaR using the full variance-covariance matrix

### Monte Carlo Simulation

- Geometric Brownian Motion (GBM)
- Configurable simulation paths and horizon
- Terminal value histogram
- Percentile fan chart visualization

---

## AI Portfolio Assistant (Local LLM)

This branch uses:

- **Ollama**
- **Model: `llama3.2`**

The assistant generates structured risk briefs using live computed metrics injected directly into the prompt.

The model is given access to:

- Portfolio holdings
- Performance metrics
- VaR / CVaR statistics
- Monte Carlo distribution outcomes
- Stress test results

Responses are deterministic and structured into:

1. Portfolio Overview
2. Key Risk Findings
3. Recommendations

No API key required.

---

## Architecture

| File      | Purpose |
|-----------|----------|
| `app.py`  | Streamlit UI and orchestration |
| `db.py`   | SQLite persistence layer |
| `data.py` | Market data ingestion (yfinance) |
| `risk.py` | Quantitative risk engine |
| `chat.py` | Prompt construction and metric injection |

The original monolithic design was refactored into modular components to improve clarity and separation of concerns.

---

## Tech Stack

- Python
- Streamlit
- Pandas / NumPy
- Plotly
- Yahoo Finance (yfinance)
- SQLite
- Ollama (local LLM)

---

## Running the App Locally

Install dependencies:

```bash
pip install -r requirements.txt

Start Ollama:

ollama serve
ollama pull llama3.2

Run the app:

streamlit run app.py

Open in browser:

http://localhost:8501
