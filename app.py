import streamlit as st
import pandas as pd
from ingestion import get_financials
from income_analysis import income_metrics
from health_analysis import classify_phase, health_score
from comparison import compare_companies, rank_companies
from visualization import (
    plot_income_trends,
    plot_growth,
    plot_revenue_comparison,
    plot_valuation_comparison
)
@st.cache_data(ttl=600)
def cached_compare(tickers):
    df = compare_companies(tickers)
    return rank_companies(df)

st.set_page_config(layout="wide")

st.title("Equity Intelligence Engine")

# -----------------------------
# Multi Ticker Selection
# -----------------------------
tickers_input = st.text_input(
    "Enter comma-separated ticker symbols",
    "AAPL,MSFT,GOOGL"
)

tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
if st.button("Analyze"):
    df = cached_compare(tuple(tickers))

    if len(tickers) == 0:
        st.warning("Please select at least one ticker.")
        st.stop()

    # =============================
    # SINGLE COMPANY VIEW
    # =============================

    primary = tickers[0]
    st.header(f"{primary} — Single Company Analysis")

    primary = tickers[0]

    income, balance, cashflow = get_financials(primary)
    metrics = income_metrics(income)

    phase = classify_phase(
        metrics["Revenue Growth"],
        metrics["Net Income Growth"]
    )

    score = health_score(income, balance)

    col1, col2 = st.columns(2)

    col1.metric("Lifecycle Phase", phase)
    col2.metric("Health Score", score)

    st.subheader("Revenue & Net Income Trend")
    st.pyplot(plot_income_trends(metrics))

    st.subheader("Growth Trend")
    st.pyplot(plot_growth(metrics))

    # =============================
    # PEER COMPARISON
    # =============================

    st.header(f"Peer Comparison: {', '.join(tickers)}")

    df = compare_companies(tickers)
    df = rank_companies(df)

    st.dataframe(df)

    st.subheader("Revenue CAGR Comparison")
    st.pyplot(plot_revenue_comparison(df))

    st.subheader("P/E Ratio Comparison")
    st.pyplot(plot_valuation_comparison(df))