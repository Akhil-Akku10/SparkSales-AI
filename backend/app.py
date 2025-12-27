from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "sales_forecast.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "..", "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURES_PATH)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API is running",
        "message": "Sales Forecasting API"
        "predicted_sales:65431.15"
    })

@app.route("/forecast", methods=["POST"])
def forecast():
    try:
        input_data = request.get_json()
        input_df = pd.DataFrame([input_data])
        input_df = input_df[feature_cols]
        prediction = model.predict(input_df)[0]
        return jsonify({
            "predicted_sales": round(float(prediction), 2),
            "model_used": "Random Forest Regressor"
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400
if __name__ == "__main__":
    app.run(debug=True)
