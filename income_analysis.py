def income_metrics(income_df):
    if "Total Revenue" not in income_df.columns or "Net Income" not in income_df.columns:
        return {
            "Revenue": None,
            "Net Income": None,
            "Revenue Growth": None,
            "Net Income Growth": None,
            "Gross Profit": income_df.get("Gross Profit", None),
            "EBIT": income_df.get("Ebit", None)
        }

    revenue = income_df["Total Revenue"]
    net_income = income_df["Net Income"]

    gross_profit = income_df.get("Gross Profit", None)
    ebit = income_df.get("Ebit", None)

    revenue_growth = revenue.pct_change()
    net_income_growth = net_income.pct_change()

    return {
        "Revenue": revenue,
        "Net Income": net_income,
        "Revenue Growth": revenue_growth,
        "Net Income Growth": net_income_growth,
        "Gross Profit": gross_profit,
        "EBIT": ebit
    }
def margin_metrics(income_df):
    revenue = income_df["Total Revenue"]
    net_income = income_df["Net Income"]

    net_margin = net_income / revenue

    return {
        "Net Margin": net_margin
    }
