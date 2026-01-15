from fastapi import FastAPI, File, UploadFile
import pandas as pd
import numpy as np
import pickle
from io import BytesIO

app = FastAPI(title="EV Battery RUL + Mode API Extended")

# Load trained model
model_path = "battery_rul_model.pkl"
with open(model_path, "rb") as f:
    model = pickle.load(f)

def compute_features(df):
    # Compute dV/dt and dI/dt
    df['dV_dt'] = df['Voltage_measured'].diff().fillna(0)
    df['dI_dt'] = df['Current_measured'].diff().fillna(0)

    # Rolling stats
    df['voltage_roll_mean'] = df['Voltage_measured'].rolling(5, min_periods=1).mean()
    df['voltage_roll_std'] = df['Voltage_measured'].rolling(5, min_periods=1).std().fillna(0)
    df['current_roll_mean'] = df['Current_measured'].rolling(5, min_periods=1).mean()
    df['current_roll_std'] = df['Current_measured'].rolling(5, min_periods=1).std().fillna(0)
    return df

def detect_mode(current):
    if current > 0.01:
        return "charging", "green"
    elif current < -0.01:
        return "discharging", "red"
    else:
        return "idle", "gray"

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))

        # Ensure necessary columns
        required_cols = ["Voltage_measured", "Current_measured"]
        for col in required_cols:
            if col not in df.columns:
                return {"error": f"Missing required column: {col}"}

        # Compute features
        df = compute_features(df)

        # Predict RUL
        feature_cols = ['Voltage_measured', 'Current_measured', 'dV_dt', 'dI_dt',
                        'voltage_roll_mean', 'voltage_roll_std',
                        'current_roll_mean', 'current_roll_std']
        df['RUL_predicted'] = model.predict(df[feature_cols])

        # Detect mode
        df[['mode', 'color']] = df['Current_measured'].apply(lambda x: pd.Series(detect_mode(x)))

        # Return JSON
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
