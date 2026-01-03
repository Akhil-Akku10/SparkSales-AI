import os
import joblib
import pandas as pd
from flask import jsonify, request

from .csv_loader import load_base_csv, load_segmented_view
from .featureeng import create_time_features, create_lag_features

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "sales_forecast.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURES_PATH)


CACHED_DF = None


def segment_forecast(request):
    try:
        if "file" not in request.files:
            return jsonify({"error": "CSV file required"}), 400
        
        df = load_base_csv(request.files["file"])

        region = request.form.get("region") or None
        category = request.form.get("category") or None
        sub_category = request.form.get("sub_category") or None

        df = load_segmented_view(df, region, category, sub_category)

        if df.empty:
            return jsonify({"error": "No data for selected segment"}), 400

        df = create_time_features(df)
        df = create_lag_features(df, target="sales")
        df = df.dropna()

        if df.empty:
            return jsonify({"error": "Insufficient data after feature engineering"}), 400

        model_features = [
            col for col in feature_cols
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col])
        ]

        X = df[model_features]

        df["predicted_sales"] = model.predict(X)

        trend_df = (
            df.groupby("order_date", as_index=False)["sales"]
              .sum()
              .sort_values("order_date")
        )

        trend = {
            "dates": trend_df["order_date"].astype(str).tolist(),
            "sales": trend_df["sales"].round(2).tolist()
        }

        last_pred = df["predicted_sales"].iloc[-1]
        forecast_quantity = [
            round(last_pred * (1 + 0.03 * i), 2)
            for i in range(1, 6)
        ]

        if len(df) >= 2 and df["sales"].iloc[-2] != 0:
            sales_growth_pct = round(
                ((df["sales"].iloc[-1] - df["sales"].iloc[-2]) / df["sales"].iloc[-2]) * 100,2)
        else:
            sales_growth_pct = 0.0
        mean_sales = df["sales"].mean()
        std_sales = df["sales"].std()

        if mean_sales == 0:
            volatility_level = "Low"
        else:
            cv = std_sales / mean_sales
            if cv > 0.5:
                volatility_level = "High"
            elif cv > 0.25:
                volatility_level = "Medium"
            else:
                volatility_level = "Low"
        kpis = {
                "latest_sales": round(df["sales"].iloc[-1], 2),
                "avg_sales": round(mean_sales, 2),
                "sales_growth_pct": sales_growth_pct,
                "volatility_level": volatility_level
        }

        return jsonify({
            "forecast_type": "Segment-wise Sales Forecast",
            "trend": trend,
            "forecast_quantity": forecast_quantity,
            "kpis": kpis
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500