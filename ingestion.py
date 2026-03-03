import yfinance as yf

def get_financials(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)

    income = ticker.financials.T
    balance = ticker.balance_sheet.T
    cashflow = ticker.cashflow.T

    income.sort_index(inplace=True)
    balance.sort_index(inplace=True)
    cashflow.sort_index(inplace=True)

    # Convert datetime index to year 
    income.index = income.index.year
    balance.index = balance.index.year
    cashflow.index = cashflow.index.year

    return income, balance, cashflow

