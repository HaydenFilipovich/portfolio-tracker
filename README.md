# Portfolio Tracker with Scenario & Stress Testing

This project is a Streamlit-based portfolio tracker that allows users to track equity holdings in real time and evaluate portfolio risk using custom scenarios and historical stress tests.

## Features

### Portfolio Tracking
- Add and remove equity holdings
- Live price data pulled from Yahoo Finance
- Automatic calculation of:
  - Market value
  - Dollar gain/loss
  - Percentage return
- Summary metrics:
  - Total portfolio value
  - Total gain/loss
  - Number of positions

### What-If Scenario Testing
- Apply a uniform market-wide price shock (−50% to +50%)
- Override individual ticker returns
- Compare:
  - Current portfolio value
  - Scenario portfolio value
  - Dollar and percentage impact

### Historical Stress Tests
Simulate portfolio performance under major historical market events:
- 2008 Financial Crisis
- COVID Crash (March 2020)
- Dot-com Bust (2000–2002)
- Black Monday (1987)
- 2022 Bear Market
- Mild correction scenario

Visualizations include:
- Bar chart comparing scenario portfolio values vs current value
- Table showing dollar losses under each scenario

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly
- Yahoo Finance (price data)

## Running the App Locally

```bash
pip install -r requirements.txt
streamlit run app.py

Then open the app in your browser at:
http://localhost:8501
