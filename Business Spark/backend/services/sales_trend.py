import pandas as pd
from flask import jsonify
import os

def compute_sales_trend(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    monthly = (
        df.resample("M", on="date")["sales"]
        .sum()
        .reset_index()
    )

    sales = monthly["sales"].astype(float)

    monthly_growth = sales.pct_change() * 100
    monthly_growth = monthly_growth.replace([float("inf"), float("-inf")], 0)
    monthly_growth = monthly_growth.fillna(0).round(2)

    
    if len(sales) >= 2 and sales.iloc[-2] != 0:
        overall_growth = ((sales.iloc[-1] - sales.iloc[-2]) / sales.iloc[-2]) * 100
    else:
        overall_growth = 0

    return {
        "trend": {
            "dates": monthly["date"].dt.strftime("%Y-%m").tolist(),
            "sales": sales.round(2).tolist(),
            "growth": monthly_growth.tolist()
        },
        "kpis": {
            "avg_sales": round(sales.mean(), 2),
            "latest_sales": round(sales.iloc[-1], 2),
            "growth_pct": round(overall_growth, 2)
        }
    }