import pandas as pd
import joblib
from flask import jsonify
import os

from .sales_trend import compute_sales_trend
from .kpi_dashboard import compute_kpis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "sales_forecast.pkl")
FEATURE_COLS_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_COLS_PATH)

#business insights
def generate_business_insights(df, prediction):
    insights = []
    avg_sales = df["sales"].mean()
    rolling_avg = df["sales"].rolling(window=7, min_periods=1).mean().iloc[-1]
    if prediction > rolling_avg * 1.15:
        insights.append(
            "Forecasted demand is significantly higher than recent trends."
        )
        inventory_action = "Increase inventory levels to meet expected demand."

    elif prediction < rolling_avg * 0.9:
        insights.append(
            "Forecasted demand is lower than recent sales patterns."
        )
        inventory_action = "Maintain or reduce inventory to prevent overstocking."

    else:
        insights.append(
            "Forecasted demand aligns closely with recent sales behavior."
        )
        inventory_action = "Maintain current inventory levels."

    insights.append(f"Inventory recommendation: {inventory_action}")
    if prediction > avg_sales:
        insights.append(
            "Positive revenue outlook based on projected sales volume."
        )
    else:
        insights.append(
            "Revenue growth may slow if current demand trends continue."
        )

    return insights
def predict_from_csv(request):
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        df = pd.read_csv(file)
        df.columns = df.columns.str.lower().str.strip()
        date_col = next((c for c in df.columns if "date" in c), None)

        if date_col is None or "sales" not in df.columns:
            return jsonify({
                "error": "CSV must contain a date column and a sales column"
            }), 400

        df = df.rename(columns={date_col: "date"})
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date", "sales"])
        df = df.sort_values("date")

        if len(df) < 5:
            return jsonify({"error": "Insufficient data for prediction"}), 400
        #trend analysis
        trend_data = compute_sales_trend(df)

        df["lag_1"] = df["sales"].shift(1)
        df["lag_2"] = df["sales"].shift(2)
        df["lag_3"] = df["sales"].shift(3)
        df["rolling_mean_3"] = df["sales"].rolling(3).mean()
        df["rolling_std_3"] = df["sales"].rolling(3).std()

        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["quarter"] = df["date"].dt.quarter

        df = df.dropna()

        if df.empty:
            return jsonify({"error": "Not enough data after feature engineering"}), 400

        latest_row = df.iloc[-1][feature_cols].values.reshape(1, -1)
        #prediction
        prediction = model.predict(latest_row)[0]
        #kpi
        kpi_data = compute_kpis(df)
        insights = generate_business_insights(df, prediction)
        expected_revenue = prediction
        trend_data=compute_sales_trend(df)
        return jsonify({
            "predicted_sales": round(float(prediction), 2),
            "expected_revenue": round(float(expected_revenue), 2),
            "trend": trend_data["trend"],
            "kpis": kpi_data,
            "insights": insights,
            "model_used": "Random Forest Regressor",
            "disclaimer": "Predictions are based on historical sales patterns and may vary."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500