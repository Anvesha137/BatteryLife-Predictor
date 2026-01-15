# Deployment Guide for EV Battery RUL Prediction API

This guide explains how to deploy the EV Battery RUL Prediction API to cloud platforms.

## Important Files

- `requirements.txt` - Contains all Python dependencies
- `Procfile` - Defines how to run the application
- `runtime.txt` - Specifies Python version
- `Dockerfile` - For containerized deployment
- `battery_rul_model.pkl` - Pre-trained model file (required for API)

## Deployment Options

### Railway

1. Sign up at railway.app
2. Connect your GitHub repository or upload your project directly
3. Railway will automatically detect the Python application from your requirements.txt
4. Make sure to include the model file (battery_rul_model.pkl) in your deployment
5. In the environment settings, ensure PORT environment variable is set
6. Deploy!

Note: If using the free tier, your application will sleep after 5 minutes of inactivity, causing slower response times on first requests.

### Render

1. Sign up at render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Select Python runtime
5. Set Root Directory to your project folder
6. Set Build Command: `pip install -r requirements.txt`
7. Set Start Command: `uvicorn battery_rul_api_extended:app --host 0.0.0.0 --port $PORT`
8. Make sure to include the model file (battery_rul_model.pkl) in your repository
9. Deploy!

Note: On the free tier, your application will sleep after 15 minutes of inactivity, resulting in slower response times on first requests.

### Google Cloud Run

1. Install Google Cloud SDK
2. Build and push the Docker image to Google Container Registry
3. Deploy to Cloud Run

## API Endpoints

- POST `/predict/` - Upload CSV data for RUL prediction and mode detection

## Notes

- The model file (battery_rul_model.pkl) is required for the API to function
- Ensure the model file is included in your deployment
- The API expects CSV files with specific columns for battery sensor data