import pandas as pd
import joblib
from flask import jsonify
import os
from services.sales_trend import compute_sales_trend

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "sales_forecast.pkl")
FEATURE_COLS_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_COLS_PATH)


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

        df = df.dropna()

        if df.empty:
            return jsonify({"error": "Not enough data to generate features"}), 400

        latest_row = df.iloc[-1][feature_cols].values.reshape(1, -1)
        prediction = model.predict(latest_row)[0]
        avg_sales = df["sales"].mean()
        inventory_action = (
            "Increase inventory" if prediction > avg_sales else "Reduce inventory"
        )

        unit_price = 1000
        expected_revenue = prediction * unit_price

        return jsonify({
            "predicted_sales": round(float(prediction), 2),
            "inventory_action": inventory_action,
            "expected_revenue": round(float(expected_revenue), 2),
            "trend": trend_data,
            "model_used": "Random Forest Regressor",
            "disclaimer": "Prediction is based on historical trends and may vary."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
