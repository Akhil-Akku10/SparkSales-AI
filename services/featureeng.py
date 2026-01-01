import pandas as pd

def create_time_features(df, date_col="order_date"):
    if date_col not in df.columns:
        raise ValueError(f"{date_col} not found in dataframe")

    df = df.sort_values(date_col)

    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["quarter"] = df[date_col].dt.quarter

    return df


def create_lag_features(df, target="sales", lags=(1, 2, 3)):
    if target not in df.columns:
        raise ValueError(f"{target} not found in dataframe")

    for lag in lags:
        df[f"lag_{lag}"] = df[target].shift(lag)

    df["rolling_mean_3"] = df[target].rolling(3, min_periods=1).mean()
    df["rolling_std_3"] = df[target].rolling(3, min_periods=1).std()

    return df