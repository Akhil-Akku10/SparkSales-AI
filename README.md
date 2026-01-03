**Business Spark – README.md**

Project Overview

Business Spark is an AI-powered sales intelligence platform designed to analyze historical sales data, generate forecasts, and provide actionable business insights through an interactive dashboard. The system combines machine learning regression models, time-series forecasting, and automated reporting to support data-driven decision making.

System Workflow Overview

Business_Spark/
│
├── backend/
│   │
│   ├── app.py                      # Flask API entry point
│   ├── __init__.py                 # Backend package initializer
│   │
│   ├── models/
│   │   ├── feature_cols.pkl         # Feature schema used by ML models
│   │   ├── sales_forecast.pkl       # Trained ML regression model
│   │   └── sarima_model.pkl         # Trained SARIMA time-series model
│   │
│   ├── reports/
│   │   ├── charts/
│   │   │   ├── historical_sales.png
│   │   │   ├── sales_trend.png
│   │   │   ├── monthly_growth.png
│   │   │   ├── growth_trend.png
│   │   │   ├── rolling_average.png
│   │   │   ├── sales_vs_rolling.png
│   │   │   └── performance_delta.png
│   │   │
│   │   └── SparkSalesReport.pdf    # Auto-generated business report
│   │
│   └── services/
│       ├── segmented_forecast.py   # Product / region-wise forecasting
│       ├── sarima_forecast.py      # Live SARIMA forecasting service
│       ├── sarima.py               # SARIMA model logic & helpers
│       ├── sales_trend.py          # Sales trends, rolling stats, growth
│       ├── pdfgen.py               # PDF report generation
│       ├── manual_forecast.py      # Manual prediction logic
│       ├── kpi_dashboard.py        # KPI calculations
│       ├── featureeng.py           # Feature engineering utilities
│       ├── csv_loader.py           # CSV ingestion and validation
│       ├── csv_formatting.py       # CSV preprocessing & cleaning
│       ├── __init__.py
│       └── __pycache__/
│
├── data/
│   │
│   ├── raw/
│   │   └── trained.csv             # Original raw dataset
│   │
│   ├── cleaned/
│   │   └── cleaned.csv             # Cleaned dataset
│   │
│   ├── processed/
│   │   └── monthly.csv             # Monthly aggregated data
│   │
│   └── sampled/
│       └── cleaned.csv             # Sample dataset for demo/testing
│
├── frontend/
│   ├── index.html                  # Main analytics dashboard
│   └── landing.html                # Landing / intro page
│
├── notebooks/
│   ├── EDA.ipynb                   # Exploratory Data Analysis
│   ├── FeatureEngineering.ipynb    # Feature engineering pipeline
│   └── Models.ipynb                # Model training & evaluation
│
├── reports/
│   └── SparkSalesReport.pdf        # Generated report copy
│
├── tests/
│   └── test_forecast.py            # Forecast service tests
│
└── README.md                       # Project documentation

The application operates through multiple analytical workflows:

1. Dataset-driven analytics and forecasting
2. Manual forecasting using lag-based inputs
3. Live time-series forecasting using SARIMA
4. Product and region-wise segmented analysis
5. Automated report generation
Each workflow is exposed through a unified dashboard and supported by a modular backend architecture.

How to run 

pip install -r requirements.txt
Backend-python -m backend.app
Frontend-Open frontend/index.html in a browser.

SARIMA Live Forecasting Dashboard Workflow

The SARIMA dashboard provides continuous time-series forecasting based on historical sales patterns.

Workflow Steps

1. Dataset Upload
The user uploads a CSV file containing historical sales data.
The backend validates and preprocesses the time-series.
2. Time-Series Preparation
Sales data is aggregated and ordered by date.
Stationarity checks and transformations are applied if required.
3. SARIMA Model Execution
A trained SARIMA model is loaded from the backend.
Forecasts are generated for a configurable number of future steps.
4. Live Forecast Updates
The dashboard periodically requests new forecasts.
Each update appends new predicted values to the live chart.
Older points are trimmed to maintain a rolling visualization window.
5. Insight Generation
Forecast trends are analyzed to detect upward, downward, or stable patterns.
Textual insights are generated alongside the visual forecast.
Output
Live-updating forecast chart
Step-wise forecast breakdown
Trend-based business insights
This workflow enables near real-time demand forecasting using classical time-series modeling.

Product and Region-wise Segmented Forecasting Workflow

The segmented forecasting module allows users to analyze sales performance across regions, categories, and sub-categories.

Workflow Steps

1. Dataset Upload
A structured sales dataset is uploaded via the dashboard.
2. Segmentation Selection
The user selects filters such as:
Region
Category
Sub-category
3. Filtered Data Extraction
The backend filters the dataset based on the selected segmentation criteria.
Validation ensures required segmentation columns are present.
4. Trend computation
Sales trends are computed for the selected segment.
5. Future Projection
Forecasts are generated for upcoming periods using historical segment data.
Results are returned as short-term projections.
6. Visualization
Segment-specific sales trends are plotted.
Forecasted values are displayed alongside historical performance.
Output
Segmented sales trend chart
Key performance indicators
Short-term forecast projections
This workflow helps identify high-performing and underperforming products or regions.

Manual Forecasting Workflow

The manual forecasting module allows users to input recent sales values directly.

Workflow Steps

1. User enters lag-based values (previous months).
2. Rolling mean and standard deviation are automatically computed.
3. Features are aligned with the trained regression model schema.
4. The ML model predicts future sales based on the provided inputs.
This mode supports scenario testing and quick forecasting without datasets.

Automated Reporting Workflow

1. All computed trends, KPIs, and forecasts are converted into charts.
2. Charts are stored in the backend reports directory.
3. A structured PDF report is generated automatically.
4. The report can be downloaded directly from the dashboard.
Technology Stack

Frontend: HTML, CSS, JavaScript, Chart.js

Backend: Flask (Python)

Machine Learning: Random Forest Regression

Time-Series Forecasting: SARIMA

Data Processing: Pandas, NumPy

Reporting: Automated PDF generation

Key Highlights

Modular service-based backend architecture

Live SARIMA forecasting with continuous updates

Product and region-wise analytical intelligence

Automatic feature engineering and validation

End-to-end pipeline from data upload to report generation



<img width="1920" height="1080" alt="Screenshot 2026-01-03 143421" src="https://github.com/user-attachments/assets/b16e8f41-e9a5-422f-8897-b930666bcf73" />
<img width="1920" height="1080" alt="Screenshot 2026-01-03 143427" 
src="https://github.com/user-attachments/assets/48a0270a-6b8f-4ab2-b90b-40d13943f963" />
<img width="1920" height="1080" alt="Screenshot 2026-01-03 143440" src="https://github.com/user-attachments/assets/a46c8107-79f3-4c37-b793-ed0fe6424302" />
<img width="1920" height="1080" alt="Screenshot 2026-01-03 143450" src="https://github.com/user-attachments/assets/57572527-39d7-40be-8feb-ac2e408cec66" />
<img width="1920" height="1080" alt="Screenshot 2026-01-03 143506" src="https://github.com/user-attachments/assets/ebb10195-4aff-419a-89d0-a3d229a90d8f" />
<img width="1920" height="1080" alt="Screenshot 2026-01-03 143514" src="https://github.com/user-attachments/assets/a59665d5-0713-4ebb-93da-329468c09db2" />
<img width="1920" height="1080" alt="Screenshot 2026-01-03 143529" src="https://github.com/user-attachments/assets/0653d7fe-d574-4c33-a1e8-a9a7848448ba" />



