import os
import pickle
import pandas as pd
from datetime import timedelta
from flask import jsonify
import numpy as np

#load the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "sarima_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model_fit = pickle.load(f)

last_date = model_fit.data.dates[-1]
def forecast_sarima(request):
    global last_date

    try:
        steps = int(request.args.get("steps", 7))
        last_date = last_date + timedelta(days=1)

        future_dates = pd.date_range(
            start=last_date,
            periods=steps,
            freq="D"
        )
        forecast = model_fit.forecast(steps=steps)

        #noise is added for depicting changes in the graph 
        noise = np.random.normal(
            0,
            forecast.std() * 0.12,
            size=len(forecast)
        )
        forecast = forecast + noise

        forecast_vals = forecast.values.astype(float)
        x = np.arange(len(forecast_vals))
        slope = np.polyfit(x, forecast_vals, 1)[0]

        slope_threshold = forecast_vals.mean() * 0.002  # adaptive

        if slope > slope_threshold:
            trend = "Increasing "
            insight = "Overall sales momentum is rising despite seasonal fluctuations."
        elif slope < -slope_threshold:
            trend = "Declining "
            insight = "Overall sales momentum is weakening across the forecast horizon."
        else:
            trend = "Stable "
            insight = "Sales demand is stable with normal seasonal oscillations."

        steps_list = [
            f"Step {i+1}: {round(val, 3)}"
            for i, val in enumerate(forecast_vals)
        ]
        return jsonify({
            "future_dates": future_dates.strftime("%Y-%m-%d").tolist(),
            "forecast": forecast_vals.tolist(),
            "steps_breakdown": steps_list,
            "insight": f"Trend detected: {trend}. {insight}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500