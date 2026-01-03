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

@app.route("/predict/manual", methods=["POST"])
def predict_manual():
    try:
        data = request.get_json()
        result = predict_sales(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/forecast", methods=["POST"])
def predict_manual_alias():
    return predict_manual()

@app.route("/forecast/csv", methods=["POST"])
def forecast_csv():
    return predict_from_csv(request)

@app.route("/download-report",methods=["POST"])
def download():
    data=request.get_json()
    pdfpath=generate_pdf_report(data)
    return send_file(pdfpath,as_attachment=True, download_name="Sales_report.pdf")

@app.route("/forecast/sarima", methods=["POST"])
def sarima_live():
    from backend.services.sarima_forecast import forecast_sarima
    return forecast_sarima(request)

@app.route("/forecast/segmented", methods=["POST"])
def forecast_segmented():
    return segment_forecast(request)

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True,use_reloader=False)
