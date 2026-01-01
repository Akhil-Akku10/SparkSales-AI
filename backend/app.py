from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
from backend.services.manuel_forecast import predict_sales
from backend.services.csv_formatting import predict_from_csv
import webbrowser
from backend.services.pdfgen import generate_pdf_report
from backend.services.sarima_forecast import forecast_sarima
from backend.services.segmented_forecast import segment_forecast

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API is running",
        "message": "SparkSales AI backend running"
    })

@app.route("/forecast", methods=["POST"])
def forecast():
    data = request.get_json()
    return predict_sales(data)

@app.route("/forecast/csv", methods=["POST"])
def forecast_csv():
    return predict_from_csv(request)

@app.route("/download-report",methods=["POST"])
def download():
    data=request.get_json()
    pdfpath=generate_pdf_report(data)
    return send_file(pdfpath,as_attachment=True, download_name="Sales_report.pdf")

@app.route("/forecast/sarima", methods=["GET"])
def sarima_forecast():
    try:
        import pickle
        import pandas as pd
        import os

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.join(BASE_DIR, "models", "sarima_model.pkl")

        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        steps = 7
        forecast = model.forecast(steps=steps)

        return jsonify({
            "model": "SARIMA",
            "horizon": steps,
            "forecast": [round(float(x), 2) for x in forecast]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/forecast/segmented", methods=["POST"])
def forecast_segmented():
    return segment_forecast(request)

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
