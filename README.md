# Equity Intelligence Engine

A Streamlit-powered financial analytics dashboard that evaluates companies across growth, profitability, capital efficiency, and valuation metrics.

This tool performs multi-company comparison using real financial statement data from Yahoo Finance and generates structured ranking scores.

**Live Demo:** [https://equity-intelligence-engine.streamlit.app](https://equity-intelligence-engine-bzgyscc82muv5pynupacc3.streamlit.app)

---

## Overview

The Equity Intelligence Engine provides:

- Revenue & Net Income trend analysis
- CAGR computation (Revenue, Net Income, FCF where applicable)
- Continuous health scoring (ROE, ROA, leverage)
- PEG-based relative valuation scoring
- Composite ranking model (Health + Valuation)
- Interactive multi-ticker web dashboard

Unlike basic finance dashboards, this engine separates:

1. **Raw financial metrics**
2. **Normalized scoring factors**
3. **Composite ranking score**

This layered structure mirrors real factor-based screening models.

---

## Features

### Single Company Analysis

- Lifecycle phase classification
- Health score (continuous)
- Revenue & income trends
- Growth acceleration visualization

### Peer Comparison

- Revenue CAGR comparison
- PEG ratio comparison
- Raw health scores
- Normalized factor scores
- Composite ranking

---

## Tech Stack

- Python
- Pandas
- NumPy
- yfinance
- Matplotlib
- Streamlit

---

## Project Structure

```
Finance/
│
├── app.py               # Main Streamlit dashboard
├── ingestion.py         # Data fetching from Yahoo Finance
├── income_analysis.py   # Income statement analysis
├── health_analysis.py   # Health scoring logic
├── comparison.py        # Multi-company comparison & ranking
├── visualization.py     # Chart generation
├── utils.py             # Helper functions
├── requirements.txt     # Dependencies
└── README.md
```

---

## Installation (Local)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DarkClown2059/equity-intelligence-engine.git
   cd equity-intelligence-engine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally:**
   ```bash
   streamlit run app.py
   ```

---

## How Scoring Works

### Health Score (Raw)

Continuous score derived from:

- Return on Equity (ROE)
- Return on Assets (ROA)
- Debt to Equity (penalized smoothly)

### Valuation Score

Relative PEG normalization across selected tickers.

### Composite Rank Score

Weighted model:

- **60% Health**
- **40% Valuation**

Raw values are preserved. Normalized values are used only for ranking.

---

## Design Philosophy

- Universal model (works across sectors)
- Robust to missing financial fields
- Never overwrites raw metrics
- Transparent scoring structure
- Modular architecture

---

## Limitations

- Relies on Yahoo Finance reported data
- PEG unstable when growth is negative
- Sector-specific nuances not yet adjusted
- Not a substitute for full DCF valuation

---

## Future Enhancements

- Factor model expansion (Quality / Growth / Value separation)
- Intrinsic valuation (DCF module)
- Risk-adjusted scoring
- Portfolio optimizer
- PDF report export
- Sector-aware scoring logic

---

## Disclaimer

> This project is for educational and research purposes only.
> **Not investment advice.**
