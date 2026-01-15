import requests

url = "http://localhost:8000/predict_rul/"
files = {"file": open(r"D:\projects\archive\cleaned_dataset\data\00001_features.csv", "rb")}  # your CSV path

response = requests.post(url, files=files)
print(response.json())
