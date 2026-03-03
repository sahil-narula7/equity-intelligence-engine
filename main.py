from ingestion import get_financials
from income_analysis import income_metrics
from health_analysis import classify_phase, health_score
from comparison import compare_companies, rank_companies, generate_summary
from visualization import (
    plot_income_trends,
    plot_growth,
    plot_revenue_comparison
)

# ==============================
# SINGLE COMPANY ANALYSIS
# ==============================

ticker = "AAPL"

income, balance, cashflow = get_financials(ticker)
metrics = income_metrics(income)

phase = classify_phase(metrics["Revenue Growth"], metrics["Net Income Growth"])
score = health_score(income, balance)

print("\n=== Single Company Analysis ===\n")
print("Company:", ticker)
print("Phase:", phase)
print("Health Score:", score)

plot_income_trends(metrics)
plot_growth(metrics)


# ==============================
# PEER COMPARISON & RANKING
# ==============================

tickers = ["AAPL", "MSFT", "GOOGL"]

df = compare_companies(tickers)
df = rank_companies(df)

print("\n=== Peer Comparison & Ranking ===\n")
print(df)

top = df.iloc[0]

print("\n=== Top Ranked Company ===")
print(generate_summary(top))

plot_revenue_comparison(df)

from visualization import plot_valuation_comparison

plot_valuation_comparison(df)