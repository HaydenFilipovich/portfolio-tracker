Portfolio Tracker with AI-Integrated Risk & Stress Testing

This project is a Streamlit-based portfolio tracker that allows users to track equity holdings in real time, evaluate portfolio risk using advanced quantitative methods, and generate AI-powered risk analysis grounded in live computed metrics.

Features
Portfolio Tracking

Add and remove equity holdings (persisted in SQLite)

CSV bulk import with template download and validation

Live price data pulled from Yahoo Finance

Automatic calculation of:

Market value

Dollar gain/loss

Percentage return

Summary metrics:

Total portfolio value

Total gain/loss

Number of positions

What-If Scenario Testing

Apply a uniform market-wide price shock (-50% to +50%)

Override individual ticker returns

Compare:

Current portfolio value

Scenario portfolio value

Dollar and percentage impact

Historical Stress Tests

Simulate portfolio performance under major historical market events using actual per-ticker peak-to-trough drawdowns:

2008 Financial Crisis

COVID Crash (March 2020)

Dot-com Bust (2000–2002)

Black Monday (1987)

2022 Bear Market

Per-ticker breakdown available in expandable panels.

Risk & Performance Analytics
Performance Metrics

Annualized return

Annualized volatility

Sharpe ratio

Sortino ratio

Maximum drawdown

Charts

Cumulative returns

Drawdown curve

Daily returns distribution

VaR / CVaR

Historical VaR & CVaR

Parametric (normal) VaR & CVaR at 90/95/99% confidence

Correlation-aware parametric VaR using the full variance-covariance matrix

Monte Carlo Simulation

Geometric Brownian Motion (GBM)

Configurable simulation paths and horizon

Terminal value histogram

Percentile fan chart visualization

AI Portfolio Assistant

The AI assistant generates a structured portfolio risk brief using live computed metrics (not static summaries).

The model is given direct access to:

Portfolio holdings

Performance metrics

VaR / CVaR statistics

Monte Carlo distribution outcomes

Stress test results

The AI explains:

Concentration risk

Volatility exposure

Tail risk

Diversification impact

Scenario sensitivity

Responses are deterministic (temperature = 0) and constrained to structured output.

AI Risk Brief — Exact Prompts

The prompts are defined in chat.py and injected with live computed metrics before each call.

System Prompt

You are a portfolio risk analyst. Given portfolio data and computed risk metrics, produce a concise risk brief.

Structure your response in exactly three sections:

Portfolio Overview
2–3 sentences summarizing portfolio composition, total value, and risk posture.

Key Risk Findings
3–5 bullet points citing specific numbers from the data. Cover concentration risk, volatility, drawdown exposure, and tail risk (VaR/CVaR). Compare Sharpe and Sortino ratios to characterize the return/risk profile.

Recommendations
2–4 bullet points with specific, actionable suggestions. Reference the data to justify each recommendation.

Rules:

Cite exact numbers from provided data.

Keep total response under 300 words.

Do not use hedging language.

Do not add disclaimers.

Branch Structure
Branch	AI Backend	Model
main	Ollama (local LLM)	llama3.2
openai	OpenAI API	gpt-4o

The main branch provides a fully local AI deployment.
The openai branch demonstrates API-based LLM integration.

Architecture

The application is modularized into focused components:

File	Purpose
app.py	Streamlit UI and orchestration
db.py	SQLite persistence layer
data.py	Market data ingestion (yfinance)
risk.py	Pure risk computations (VaR, Monte Carlo, etc.)
chat.py	AI prompt construction and metric injection

The original monolithic design was refactored into modular components to improve clarity, extensibility, and separation of concerns.

Tech Stack

Python

Streamlit

Pandas / NumPy

Plotly

Yahoo Finance (yfinance)

SQLite (persistence)

Ollama (local LLM, main branch)

OpenAI API (optional, openai branch)

Running the App Locally
Install dependencies:
pip install -r requirements.txt
Run the app:
streamlit run app.py
For main branch (Ollama)
ollama serve
ollama pull llama3.2
For openai branch

Create a .env file:

OPENAI_API_KEY=your-key-here

Then run:

streamlit run app.py

Open in your browser at:

http://localhost:8501
