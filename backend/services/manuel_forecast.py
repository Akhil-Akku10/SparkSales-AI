import joblib
import pandas as pd
import os
from flask import jsonify

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "sales_forecast.pkl")
FEATURE_COLS_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_COLS_PATH)

def predict_sales(input_data):
    try:
        df = pd.DataFrame([input_data])
        df = df[feature_cols]

        prediction = model.predict(df)[0]

        return jsonify({
            "predicted_sales": round(float(prediction), 2),
            "model_used": "Random Forest Regressor",
            "disclaimer": "Prediction is based on historical trends and may vary."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
