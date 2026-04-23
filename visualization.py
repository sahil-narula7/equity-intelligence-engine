import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


# -----------------------------
# Revenue & Net Income Trend
# -----------------------------
def plot_income_trends(metrics):
    revenue = metrics["Revenue"] / 1e9
    net_income = metrics["Net Income"] / 1e9

    years = revenue.index

    plt.figure(figsize=(8, 5))
    plt.plot(years, revenue, marker='o', label="Revenue")
    plt.plot(years, net_income, marker='o', label="Net Income")

    plt.title("Revenue & Net Income Trend", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("Amount (Billions USD)")
    plt.legend()
    plt.tight_layout()
    return plt.gcf()


# -----------------------------
# Growth Trend
# -----------------------------
def plot_growth(metrics):
    rev_growth = metrics["Revenue Growth"]
    ni_growth = metrics["Net Income Growth"]

    years = rev_growth.index

    plt.figure(figsize=(8, 5))
    plt.plot(years, rev_growth, marker='o', label="Revenue Growth")
    plt.plot(years, ni_growth, marker='o', label="Net Income Growth")

    plt.title("Growth Trend", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("Growth Rate")
    plt.legend()

    # Format as percentage
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # Annotation for latest Net Income acceleration
    if len(ni_growth) >= 2:
        latest_growth = ni_growth.iloc[-1]
        annotation_text = "Net Income Grows!" if latest_growth > 0 else "Net Income Declines"
        plt.annotate(
            annotation_text,
            xy=(years[-1], latest_growth),
            xytext=(years[-2], latest_growth * 0.7),
            arrowprops=dict(arrowstyle="->")
        )

    plt.tight_layout()
    return plt.gcf()


# -----------------------------
# Revenue CAGR Comparison
# -----------------------------
def plot_revenue_comparison(df):
    plt.figure(figsize=(8, 5))

    bars = plt.bar(df["Company"], df["Revenue CAGR"])

    plt.title("Revenue CAGR Comparison", fontsize=14)
    plt.ylabel("Revenue CAGR")

    # Format axis as %
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1%}",
            ha='center',
            va='bottom'
        )

    plt.tight_layout()
    return plt.gcf()


# -----------------------------
# ROE Trend
# -----------------------------
def plot_roe(roe_series):
    plt.figure(figsize=(8, 5))
    plt.plot(roe_series.index, roe_series, marker='o')

    plt.title("Return on Equity Trend", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("ROE")

    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    plt.tight_layout()
    return plt.gcf()

# -----------------------------
# Valuation Comparison (P/E)
# -----------------------------
def plot_valuation_comparison(df):
    plt.figure(figsize=(8, 5))

    pe_values = pd.to_numeric(df["P/E Ratio"], errors="coerce")

    if pe_values.dropna().empty:
        plt.title("P/E Ratio Comparison", fontsize=14)
        plt.ylabel("P/E Ratio")
        plt.xticks(range(len(df["Company"])), df["Company"])
        plt.text(
            0.5,
            0.5,
            "No P/E data available for selected tickers.",
            ha="center",
            va="center",
            transform=plt.gca().transAxes
        )
        plt.tight_layout()
        return plt.gcf()

    bars = plt.bar(df["Company"], pe_values)

    plt.title("P/E Ratio Comparison", fontsize=14)
    plt.ylabel("P/E Ratio")

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}",
                ha='center',
                va='bottom'
            )

    plt.tight_layout()
    return plt.gcf()