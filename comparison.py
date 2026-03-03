import pandas as pd
import yfinance as yf
from ingestion import get_financials
from income_analysis import income_metrics
from health_analysis import classify_phase, health_score
from utils import calculate_cagr, get_column


def analyze_company(ticker):

    income, balance, cashflow = get_financials(ticker)
    metrics = income_metrics(income)

    # ---------- SAFE P/E ----------
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        pe_ratio = info.get("trailingPE", None)
    except Exception:
        pe_ratio = None

    # ---------- Growth ----------
    rev_cagr = calculate_cagr(metrics["Revenue"])
    ni_cagr = calculate_cagr(metrics["Net Income"])

    peg_ratio = None
    if pe_ratio and rev_cagr and rev_cagr > 0:
        peg_ratio = pe_ratio / (rev_cagr * 100)

    # ---------- Profitability ----------
    net_margin_series = income["Net Income"] / income["Total Revenue"]
    net_margin_avg = net_margin_series.mean()

    equity = get_column(balance, [
        "Stockholders Equity",
        "Common Stock Equity",
        "Total Equity Gross Minority Interest"
    ])

    roe_avg = None
    if equity is not None:
        roe_series = income["Net Income"] / equity
        roe_avg = roe_series.mean()

    # ---------- Cash Flow ----------
    ocf = get_column(cashflow, [
        "Total Cash From Operating Activities",
        "Operating Cash Flow",
        "Net Cash Provided By Operating Activities"
    ])

    capex = get_column(cashflow, [
        "Capital Expenditures",
        "Capital Expenditure",
        "Purchase Of PPE"
    ])

    fcf_cagr = None
    if ocf is not None and capex is not None:
        fcf = ocf - capex
        fcf_cagr = calculate_cagr(fcf)

    # ---------- Classification ----------
    phase = classify_phase(
        metrics["Revenue Growth"],
        metrics["Net Income Growth"]
    )

    score = health_score(income, balance)

    return {
        "Company": ticker,
        "Revenue CAGR": rev_cagr,
        "Net Income CAGR": ni_cagr,
        "FCF CAGR": fcf_cagr,
        "Net Margin Avg": net_margin_avg,
        "ROE Avg": roe_avg,
        "Phase": phase,
        "Health Score": score,
        "P/E Ratio": pe_ratio,
        "PEG Ratio": peg_ratio
    }


def compare_companies(tickers):

    results = []

    for ticker in tickers:
        results.append(analyze_company(ticker))

    return pd.DataFrame(results)