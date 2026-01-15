# File: D:\projects\archive\battery_rul_api.py

from fastapi import FastAPI, UploadFile, File
import pandas as pd
import pickle
from io import BytesIO

# Paths
MODEL_PATH = r"D:\projects\archive\battery_rul_model.pkl"

# Load model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

app = FastAPI(title="Battery RUL Predictor")

@app.post("/predict_rul/")
async def predict_rul(file: UploadFile = File(...)):
    """
    Upload a CSV with columns:
    ['Voltage_measured','Current_measured','dV_dt','dI_dt',
     'voltage_roll_mean','voltage_roll_std','current_roll_mean',
     'current_roll_std']
    Returns predicted RUL for each row.
    """
    try:
        # Read uploaded CSV
        content = await file.read()
        df = pd.read_csv(BytesIO(content))

        # Check required columns
        required_cols = [
            "Voltage_measured","Current_measured","dV_dt","dI_dt",
            "voltage_roll_mean","voltage_roll_std","current_roll_mean",
            "current_roll_std"
        ]
        missing = set(required_cols) - set(df.columns)
        if missing:
            return {"error": f"Missing columns: {missing}"}

        # Predict RUL
        df["RUL_predicted"] = model.predict(df[required_cols])

        # Return as JSON
        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# Run with:
# uvicorn battery_rul_api:app --reload --host 0.0.0.0 --port 8000
