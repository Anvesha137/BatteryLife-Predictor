import pandas as pd
import numpy as np

# Load CSV
df = pd.read_csv(r"D:\projects\archive\cleaned_dataset\data\00001.csv")

# Sort by time
df = df.sort_values("Time").reset_index(drop=True)

# Compute dV/dt and dI/dt
df["dV_dt"] = df["Voltage_measured"].diff() / df["Time"].diff()
df["dI_dt"] = df["Current_measured"].diff() / df["Time"].diff()

# Rolling stats
df["voltage_roll_mean"] = df["Voltage_measured"].rolling(5).mean()
df["voltage_roll_std"] = df["Voltage_measured"].rolling(5).std()
df["current_roll_mean"] = df["Current_measured"].rolling(5).mean()
df["current_roll_std"] = df["Current_measured"].rolling(5).std()

# Fill NaNs
df = df.fillna(0)

# Estimate cumulative capacity as energy (voltage*current*delta_time)
df["delta_time"] = df["Time"].diff().fillna(0)
df["capacity_est"] = (df["Voltage_measured"] * df["Current_measured"] * df["delta_time"]).cumsum()

# Compute RUL proxy: assume 80% of max capacity as EOL
initial_capacity = df["capacity_est"].max()
eol_threshold = 0.8 * initial_capacity
df["RUL"] = eol_threshold - df["capacity_est"]
df["RUL"] = df["RUL"].clip(lower=0)  # no negatives

# Aggregate features per 50 time steps (optional, speeds up ML)
features = df.groupby(df.index // 50).agg({
    "Voltage_measured": "mean",
    "Current_measured": "mean",
    "dV_dt": "mean",
    "dI_dt": "mean",
    "voltage_roll_mean": "mean",
    "voltage_roll_std": "mean",
    "current_roll_mean": "mean",
    "current_roll_std": "mean",
    "RUL": "first"
}).reset_index(drop=True)

# Save for ML
features.to_csv(r"D:\projects\archive\cleaned_dataset\data\00001_features.csv", index=False)
print("Feature CSV ready for ML!")
