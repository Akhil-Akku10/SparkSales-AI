import os
import pickle
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

# ==============================
# PATH SETUP
# ==============================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "cleaned", "clean.csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "backend", "models", "sarima_model.pkl")

print("PROJECT_ROOT:", PROJECT_ROOT)
print("DATA_PATH:", DATA_PATH)
print("Exists:", os.path.exists(DATA_PATH))

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.lower().str.strip()

# ==============================
# DATE COLUMN HANDLING
# ==============================
if "order date" in df.columns:
    df = df.rename(columns={"order date": "date"})
elif "order_date" in df.columns:
    df = df.rename(columns={"order_date": "date"})
elif "ship date" in df.columns:
    df = df.rename(columns={"ship date": "date"})
else:
    raise ValueError("No valid date column found")

if "sales" not in df.columns:
    raise ValueError("Sales column not found")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date", "sales"])

# ==============================
# AGGREGATE DAILY SALES (IMPORTANT)
# ==============================
df = df.groupby("date", as_index=False)["sales"].sum()

# ==============================
# SET DATE INDEX & FREQUENCY
# ==============================
df = df.sort_values("date")
df.set_index("date", inplace=True)

# Daily frequency (fill missing days with 0 sales)
df = df.asfreq("D", fill_value=0)

sales = df["sales"]

print("Final rows:", len(sales))
print("Duplicate dates:", sales.index.duplicated().sum())

# ==============================
# TRAIN SARIMA MODEL
# ==============================
model = SARIMAX(
    sales,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)

model_fit = model.fit(disp=False)

# ==============================
# SAVE MODEL
# ==============================
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model_fit, f)

print("SARIMA model saved to:", MODEL_PATH)