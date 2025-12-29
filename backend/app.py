from flask import Flask, request, jsonify
from flask_cors import CORS
from services.manuel_forecast import predict_sales
from services.csv_formatting import predict_from_csv
import webbrowser

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

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
