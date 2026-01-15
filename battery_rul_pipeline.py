# File: D:\projects\archive\battery_rul_pipeline.py

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# -------------------------------
# 1. Load the feature dataset
# -------------------------------
csv_path = r"D:\projects\archive\cleaned_dataset\data\00001_features.csv"  # Update path if needed
df = pd.read_csv(csv_path)

# Inspect columns
print("Columns:", df.columns.tolist())

# -------------------------------
# 2. Prepare features and target
# -------------------------------
X = df.drop("RUL", axis=1)
y = df["RUL"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# 3. Train XGBoost regressor
# -------------------------------
model = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42)
model.fit(X_train, y_train)

# -------------------------------
# 4. Predict & evaluate
# -------------------------------
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2:", r2_score(y_test, y_pred))

# -------------------------------
# 5. Save trained model
# -------------------------------
model_path = r"D:\projects\archive\battery_rul_model.pkl"
joblib.dump(model, model_path)
print(f"Model saved at: {model_path}")
