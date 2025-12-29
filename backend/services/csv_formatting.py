import pandas as pd
import joblib
from flask import jsonify
import os
from services.sales_trend import compute_sales_trend
from services.kpi_dashboard import compute_kpis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "sales_forecast.pkl")
FEATURE_COLS_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_COLS_PATH)
def generate_business_insights(df, prediction):
    insights = []

    # Trend insight
    last_3 = df["sales"].tail(3).mean()
    prev_3 = df["sales"].iloc[-6:-3].mean() if len(df) >= 6 else last_3

    if last_3 > prev_3:
        insights.append("Sales trend is increasing")
    elif last_3 < prev_3:
        insights.append("Sales trend is declining")
    else:
        insights.append(" Sales trend is stable")

 
    volatility = df["sales"].rolling(3).std().mean()
    avg_sales=df['sales'].mean()
    if volatility > avg_sales * 0.3:
        level="High"
        insights.append("High demand volatility detected")
    elif volatility>avg_sales*0.2:
        insights.append("Moderate demand volatility. Please be careful")
        level="Moderate"
    else:
        level="Low"
        insights.append("Low demand volatility. Dont worry Sales demands are stable")
    if prediction>avg_sales*1.1 and level=="Low":
        inrecom="I recommend to strongly increase your inventory"
    elif prediction>avg_sales and level in ["High","Moderate"]:
        inrecom="Please be cautious while increasing the inventory"
    elif abs(prediction-avg_sales)/avg_sales<0.1:
        inrecom="Please maintain your current inventory level. Dont increase or decrease the storage"
    else:
        inrecom="Reduce the inventory to avoid overstocking"
    insights.append(f"Inventory recommendation:{inrecom}")
    if prediction > avg_sales:
        insights.append(" Revenue growth opportunity detected")
    else:
        insights.append(" Potential revenue risk detected")

    return insights
def predict_from_csv(request):
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        df = pd.read_csv(file)
        df.columns = df.columns.str.lower().str.strip()
        date_col = None
        for col in df.columns:
            if "date" in col:
                date_col = col
                break

        if date_col is None or "sales" not in df.columns:
            return jsonify({
                "error": "CSV must contain a date column and a sales column"
            }), 400

        df = df.rename(columns={date_col: "date"})
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date", "sales"])
        df = df.sort_values("date")

        trend_data = compute_sales_trend(df)
        df["lag_1"] = df["sales"].shift(1)
        df["lag_2"] = df["sales"].shift(2)
        df["lag_3"] = df["sales"].shift(3)
        df["rolling_mean_3"] = df["sales"].rolling(3).mean()
        df["rolling_std_3"] = df["sales"].rolling(3).std()
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["quarter"] = df["date"].dt.quarter

        if df.empty:
            return jsonify({"error": "Not enough data to generate features"}), 400

        latest_row = df.iloc[-1][feature_cols].values.reshape(1, -1)
        total_sales=df['sales'].sum()
        prediction = model.predict(latest_row)[0]
        avg_sales = df["sales"].mean()
        inventory_action = (
            "Increase inventory" if prediction > avg_sales else "Reduce inventory"
        )

        unit_price = 1000
        expected_revenue = prediction * unit_price
        insights=generate_business_insights(df,prediction)
        kpi_data=compute_kpis(df)

        return jsonify({
            "predicted_sales": round(float(prediction), 2),
            "inventory_action": inventory_action,
            "expected_revenue": round(float(expected_revenue), 2),
            "trend": trend_data,
            "kpis":kpi_data,
            "insights": insights,
            "model_used": "Random Forest Regressor",
            "disclaimer": "Prediction is based on historical trends and may vary."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    