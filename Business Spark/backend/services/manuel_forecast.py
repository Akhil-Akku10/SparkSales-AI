import joblib
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "sales_forecast.pkl")
FEATURE_COLS_PATH = os.path.join(BASE_DIR, "models", "feature_cols.pkl")

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_COLS_PATH)
#sales prediction
def predict_sales(input_data):
    try:
        l1 = float(input_data.get("lag_1", 0))
        l2 = float(input_data.get("lag_2", 0))
        l3 = float(input_data.get("lag_3", 0))

        year = int(input_data.get("year", 0))
        month = int(input_data.get("month", 0))
        quarter = int(input_data.get("quarter", 0))
        rolling_mean = (l1 + l2 + l3) / 3

        rolling_std = (
            ((l1 - rolling_mean) ** 2 +
             (l2 - rolling_mean) ** 2 +
             (l3 - rolling_mean) ** 2) / 3
        ) ** 0.5

        scale = max(1, 10000 / max(rolling_mean, 1))
        rolling_mean *= scale
        rolling_std *= scale

        row = {
            "lag_1": l1,
            "lag_2": l2,
            "lag_3": l3,
            "rolling_mean_3": rolling_mean,
            "rolling_std_3": rolling_std,
            "year": year,
            "month": month,
            "quarter": quarter
        }

        df = pd.DataFrame([[row[col] for col in feature_cols]],
                          columns=feature_cols)

        df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

        prediction = model.predict(df)[0]

        return {
            "predicted_sales": round(float(prediction), 2),
            "rolling_mean": round(rolling_mean, 2),
            "rolling_std": round(rolling_std, 2),
            "model_used": "Random Forest Regressor",
            "note": "Rolling statistics computed automatically"
        }

    except Exception as e:
        raise RuntimeError(f"Manual prediction failed: {str(e)}")