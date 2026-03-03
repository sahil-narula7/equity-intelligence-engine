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
        # Try multiple keys for P/E ratio
        pe_ratio = info.get("trailingPE") or info.get("forwardPE") or info.get("pegRatio")
        # If still None, calculate from price and EPS
        if pe_ratio is None:
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            eps = info.get("trailingEps")
            if price and eps and eps > 0:
                pe_ratio = price / eps
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


def rank_companies(df):
    """
    Rank companies based on key metrics.
    Higher scores indicate better investment potential.
    """
    ranked = df.copy()

    # Rank by each metric (higher is better for most)
    rank_cols = []

    if "Revenue CAGR" in ranked.columns:
        ranked["Revenue CAGR Rank"] = ranked["Revenue CAGR"].rank(ascending=False, na_option="bottom")
        rank_cols.append("Revenue CAGR Rank")

    if "Net Income CAGR" in ranked.columns:
        ranked["NI CAGR Rank"] = ranked["Net Income CAGR"].rank(ascending=False, na_option="bottom")
        rank_cols.append("NI CAGR Rank")

    if "FCF CAGR" in ranked.columns:
        ranked["FCF CAGR Rank"] = ranked["FCF CAGR"].rank(ascending=False, na_option="bottom")
        rank_cols.append("FCF CAGR Rank")

    if "Net Margin Avg" in ranked.columns:
        ranked["Margin Rank"] = ranked["Net Margin Avg"].rank(ascending=False, na_option="bottom")
        rank_cols.append("Margin Rank")

    if "ROE Avg" in ranked.columns:
        ranked["ROE Rank"] = ranked["ROE Avg"].rank(ascending=False, na_option="bottom")
        rank_cols.append("ROE Rank")

    if "Health Score" in ranked.columns:
        ranked["Health Rank"] = ranked["Health Score"].rank(ascending=False, na_option="bottom")
        rank_cols.append("Health Rank")

    # Lower PEG is better
    if "PEG Ratio" in ranked.columns:
        ranked["PEG Rank"] = ranked["PEG Ratio"].rank(ascending=True, na_option="bottom")
        rank_cols.append("PEG Rank")

    # Calculate overall rank as average of individual ranks
    if rank_cols:
        ranked["Overall Rank"] = ranked[rank_cols].mean(axis=1).rank(ascending=True)
        ranked = ranked.sort_values("Overall Rank")

    return ranked