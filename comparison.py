import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from ingestion import get_financials
from income_analysis import income_metrics
from health_analysis import classify_phase, health_score
from utils import calculate_cagr, get_column


def analyze_company(ticker):
    income, balance, cashflow = get_financials(ticker)
    metrics = income_metrics(income)
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info

    pe_ratio = info.get("trailingPE", None)

    # --- Growth Metrics ---
    rev_cagr = calculate_cagr(metrics["Revenue"])
    ni_cagr = calculate_cagr(metrics["Net Income"])

    peg_ratio = None
    if pe_ratio and rev_cagr and rev_cagr > 0:
        peg_ratio = pe_ratio / (rev_cagr * 100)

    # --- Profitability Metrics ---
    net_margin_series = income["Net Income"] / income["Total Revenue"]
    net_margin_avg = net_margin_series.mean()

    equity = get_column(balance, [
        "Stockholders Equity",
        "Common Stock Equity",
        "Total Equity Gross Minority Interest"
    ])

    roe_series = income["Net Income"] / equity
    roe_avg = roe_series.mean()

    # --- Cash Flow Metric ---
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

    if ocf is not None and capex is not None:
        fcf = ocf - capex
        fcf_cagr = calculate_cagr(fcf)
    else:
        fcf_cagr = None

    # --- Classification & Health ---
    phase = classify_phase(metrics["Revenue Growth"], metrics["Net Income Growth"])
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

    df = pd.DataFrame(results)

    return df


def rank_companies(df):

    df = df.copy()

    # ---------- Valuation Score (RAW) ----------
    if "PEG Ratio" in df.columns and df["PEG Ratio"].notna().any():

        valid_pegs = df["PEG Ratio"].dropna()

        if len(valid_pegs) > 1:
            max_peg = valid_pegs.max()
            min_peg = valid_pegs.min()

            df["Valuation Score Raw"] = df["PEG Ratio"].apply(
                lambda x: (max_peg - x) / (max_peg - min_peg)
                if pd.notna(x) and max_peg != min_peg else 0
            )
        else:
            df["Valuation Score Raw"] = 0
    else:
        df["Valuation Score Raw"] = 0

    # ---------- Normalize Health (DO NOT OVERWRITE RAW) ----------
    if df["Health Score"].max() != df["Health Score"].min():
        df["Health Score Normalized"] = (
            df["Health Score"] - df["Health Score"].min()
        ) / (
            df["Health Score"].max() - df["Health Score"].min()
        )
    else:
        df["Health Score Normalized"] = 0

    # ---------- Normalize Valuation ----------
    if df["Valuation Score Raw"].max() != df["Valuation Score Raw"].min():
        df["Valuation Score Normalized"] = (
            df["Valuation Score Raw"] - df["Valuation Score Raw"].min()
        ) / (
            df["Valuation Score Raw"].max() - df["Valuation Score Raw"].min()
        )
    else:
        df["Valuation Score Normalized"] = 0

    # ---------- Composite ----------
    df["Rank Score"] = (
        0.6 * df["Health Score Normalized"] +
        0.4 * df["Valuation Score Normalized"]
    )

    return df.sort_values(by="Rank Score", ascending=False)

def plot_valuation_comparison(df):
    plt.figure(figsize=(8, 5))

    bars = plt.bar(df["Company"], df["P/E Ratio"])

    plt.title("P/E Ratio Comparison", fontsize=14)
    plt.ylabel("P/E Ratio")

    for bar in bars:
        height = bar.get_height()
        if height:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{height:.1f}",
                ha='center',
                va='bottom'
            )

    plt.tight_layout()
    plt.show()

def generate_summary(row):
    return f"""
{row['Company']} Analysis Summary:
Revenue CAGR: {row['Revenue CAGR']:.2%}
Net Income CAGR: {row['Net Income CAGR']:.2%}
FCF CAGR: {row['FCF CAGR']:.2%}
Average Net Margin: {row['Net Margin Avg']:.2%}
Average ROE: {row['ROE Avg']:.2%}
Phase Classification: {row['Phase']}
Health Score: {row['Health Score']}
Overall Rank Score: {row['Rank Score']}
"""