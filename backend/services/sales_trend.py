import pandas as pd
from flask import jsonify
import os

def compute_sales_trend(df):
   
    monthly = (
        df.resample("M", on="date")["sales"]
        .sum()
        .reset_index()
    )

    
    monthly["growth"] = monthly["sales"].pct_change() * 100

    
    monthly = monthly.replace([float("inf"), float("-inf")], 0)
    monthly = monthly.fillna(0)

    return {
        "dates": monthly["date"].dt.strftime("%Y-%m").tolist(),
        "sales": monthly["sales"].round(2).tolist(),
        "growth": monthly["growth"].round(2).tolist()
    }
