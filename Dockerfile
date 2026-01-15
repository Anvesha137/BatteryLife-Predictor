FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port the app runs on
EXPOSE $PORT 8000

# Run the application
CMD ["uvicorn", "battery_rul_api_extended:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]