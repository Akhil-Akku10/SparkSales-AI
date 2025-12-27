import requests
import json

URL = "http://127.0.0.1:5000/forecast"

payload = {
    "year": 2024,
    "month": 9,
    "quarter": 3,
    "lag_1": 85000,
    "lag_2": 83000,
    "lag_3": 81000,
    "rolling_mean_3": 83000,
    "rolling_std_3": 1200
}

try:
    response = requests.post(URL, json=payload)

    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=4))

except Exception as e:
    print("Error calling API:", e)
