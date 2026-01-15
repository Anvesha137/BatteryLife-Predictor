# EV Battery Remaining Useful Life (RUL) Prediction System

This project provides a machine learning-based solution for predicting the Remaining Useful Life (RUL) of electric vehicle (EV) batteries. It includes data processing pipelines, a trained model, API endpoints, and a dashboard for visualization.

## Overview

The system predicts the remaining useful life of EV batteries by analyzing various sensor readings such as voltage, current, temperature, and time measurements. The solution includes:

- Data preprocessing pipeline for battery sensor data
- Machine learning model trained to predict RUL
- REST API for RUL predictions
- Interactive dashboard for data visualization
- Mode detection (charging/discharging/idle states)

## Architecture

The project consists of the following components:

1. **Data Processing Scripts**:
   - `battery_rul.py`: Preprocesses raw battery data and extracts features
   - `battery_rul_pipeline.py`: Trains the ML model and saves it

2. **ML Model**:
   - `battery_rul_model.pkl`: Trained XGBoost model for RUL prediction

3. **API Services**:
   - `battery_rul_api.py`: Basic API for RUL predictions
   - `battery_rul_api_extended.py`: Extended API with mode detection

4. **Visualization**:
   - `ev_battery_rul_dashboard.py`: Streamlit dashboard for interactive analysis

5. **Testing**:
   - `test_rul.py`: Test script

## Prerequisites

- Python 3.7+
- Dependencies listed in requirements.txt (if available)
- Pandas, NumPy, scikit-learn, XGBoost, FastAPI, Streamlit

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install pandas numpy scikit-learn xgboost fastapi streamlit uvicorn
   ```
3. Place your battery data in the `cleaned_dataset/data/` directory

## Usage

### 1. Data Preprocessing

Process raw battery data:
```bash
python battery_rul.py
```

### 2. Model Training

Train the RUL prediction model:
```bash
python battery_rul_pipeline.py
```

### 3. Running the API

Start the RUL prediction API:
```bash
uvicorn battery_rul_api_extended:app --reload --host 0.0.0.0 --port 8000
```

### 4. Using the Dashboard

Launch the interactive dashboard:
```bash
streamlit run ev_battery_rul_dashboard.py
```

### 5. Making Predictions

Upload a CSV file containing the following columns:
- Voltage_measured
- Current_measured
- Temperature_measured
- Current_load
- Voltage_load
- Time

The API will compute derived features and return RUL predictions along with battery mode classification (charging, discharging, or idle).

## API Endpoints

- POST `/predict/` - Upload CSV data for RUL prediction and mode detection

## Features

- Real-time RUL prediction based on battery sensor data
- Automatic feature engineering (derivatives, rolling statistics)
- Battery mode detection (charging/discharging/idle)
- Interactive visualization dashboard
- Scalable API for batch predictions

## Data Schema

Input CSV should contain the following columns:
- `Voltage_measured`: Measured voltage
- `Current_measured`: Measured current
- `Temperature_measured`: Measured temperature
- `Current_load`: Load current
- `Voltage_load`: Load voltage
- `Time`: Timestamp

## Model Performance

The XGBoost model is trained with the following configuration:
- n_estimators: 200
- learning_rate: 0.05
- max_depth: 4
- random_state: 42

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.