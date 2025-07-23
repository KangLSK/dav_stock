def add_ma(df, window=(5,20,60)):
    for w in window:
        df[f"MA{w}"] = df["close"].rolling(w).mean()
    return df
