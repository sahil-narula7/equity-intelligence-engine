def get_column(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return df[name]
    return None

def calculate_cagr(series):
    import pandas as pd
    # Convert to pandas Series if not 
    if not isinstance(series, pd.Series):
        try:
            series = pd.Series(series)
        except Exception:
            return 0
    series = series.dropna()

    if len(series) < 2:
        return 0

    start = series.iloc[0]
    end = series.iloc[-1]
    years = len(series) - 1

    if start <= 0:
        return 0

    return (end / start) ** (1 / years) - 1
