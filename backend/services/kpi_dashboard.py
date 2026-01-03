import numpy as np

def compute_kpis(df):
    """
     KPI metrics
    """

    total_sales = df["sales"].sum()
    avg_sales = df["sales"].mean()
    latest_sales = df["sales"].iloc[-1]

    if len(df) > 1:
        prev = df["sales"].iloc[-2]
        sales_growth_pct = ((latest_sales - prev) / prev) * 100 if prev != 0 else 0
    else:
        sales_growth_pct = 0

    std_dev = df["sales"].std()
    volatility_ratio = std_dev / avg_sales if avg_sales != 0 else 0

    if volatility_ratio > 0.35:
        volatility_level = "High"
    elif volatility_ratio > 0.20:
        volatility_level = "Medium"
    else:
        volatility_level = "Low"

    return {
        "total_sales": round(float(total_sales), 2),
        "avg_sales": round(float(avg_sales), 2),
        "latest_sales": round(float(latest_sales), 2),
        "sales_growth_pct": round(float(sales_growth_pct), 2),
        "volatility_level": volatility_level
    }
