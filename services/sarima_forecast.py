import pickle
import pandas as pd
import os
from flask import jsonify, request

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "sarima_model.pkl")

# Load trained SARIMA model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def forecast_sarima(request):
    """
    Live SARIMA forecasting
    Input: forecast_steps (optional)
    Output: future dates + predictions
    """

    try:
        steps = int(request.args.get("steps", 7))  # default 7 days

        forecast = model.get_forecast(steps=steps)
        predictions = forecast.predicted_mean.round(2)

        last_date = model.data.dates[-1]
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=steps,
            freq="D"
        )

        return jsonify({
            "model": "SARIMA",
            "forecast_horizon": f"{steps} days",
            "future_dates": future_dates.strftime("%Y-%m-%d").tolist(),
            "predicted_sales": predictions.tolist(),
            "note": "Forecast based on historical order date sales"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500