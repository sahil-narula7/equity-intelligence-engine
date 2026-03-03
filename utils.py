def calculate_cagr(series):
    start = series.iloc[0]
    end = series.iloc[-1]
    years = len(series) - 1
    return (end / start) ** (1 / years) - 1

def get_column(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return df[name]
    return None

def calculate_cagr(series):
    series = series.dropna()

    if len(series) < 2:
        return 0

    start = series.iloc[0]
    end = series.iloc[-1]
    years = len(series) - 1

    if start <= 0:
        return 0

    return (end / start) ** (1 / years) - 1