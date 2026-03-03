import numpy as np

def classify_phase(revenue_growth, net_income_growth):
    avg_rev_growth = revenue_growth.mean()
    avg_income_growth = net_income_growth.mean()

    if avg_rev_growth > 0.15 and avg_income_growth > 0.15:
        return "High Growth Phase"
    elif 0.05 <= avg_rev_growth <= 0.15:
        return "Mature Stable Phase"
    elif avg_rev_growth < 0:
        return "Decline Phase"
    else:
        return "Transitional Phase"

def health_score(income, balance):

    net_income = income["Net Income"]
    total_assets = balance["Total Assets"]

    def get_column(df, possible_names):
        for name in possible_names:
            if name in df.columns:
                return df[name]
        return None

    total_equity = get_column(balance, [
        "Stockholders Equity",
        "Common Stock Equity",
        "Total Equity Gross Minority Interest"
    ])

    total_debt = get_column(balance, [
        "Total Debt",
        "Long Term Debt",
        "Long Term Debt And Capital Lease Obligation"
    ])

    if total_equity is None or total_debt is None:
        return 0

    roe = (net_income / total_equity).mean()
    roa = (net_income / total_assets).mean()
    debt_equity = (total_debt / total_equity).mean()

    # Continuous scoring
    roe_score = max(roe, 0)
    roa_score = max(roa, 0)
    leverage_score = 1 / (1 + max(debt_equity, 0))

    score = roe_score + roa_score + leverage_score

    return score