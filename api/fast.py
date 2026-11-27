from fastapi import FastAPI
import os
import pandas as pd
from dotenv import load_dotenv
from google.cloud import storage
from src.taxifare.predict import predict, load_model
load_dotenv()

app = FastAPI(title="taxifare")

# MODEL_PATH = os.getenv("MODEL_PATH")
# model = load_model(MODEL_PATH)

MODEL_SOURCE = os.getenv("MODEL_SOURCE", "local")
MODEL_PATH = os.getenv("MODEL_PATH", "models/linreg_pipeline.joblib")

if MODEL_SOURCE == "gcs":
    destination = os.environ["DESTINATION_FILE_NAME"]
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    storage.Client().bucket(os.environ["BUCKET_NAME"]) \
        .blob(os.environ["SOURCE_BLOB_NAME"]) \
        .download_to_filename(destination)
    MODEL_PATH = destination

model = load_model(MODEL_PATH)

@app.get("/")
def root():
    return {"message": "Taxifare API is running"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}

@app.get("/predict")
def prediction(
    pickup_datetime: str,
    pickup_longitude: float,
    pickup_latitude: float,
    dropoff_longitude: float,
    dropoff_latitude: float,
    passenger_count: int,
):
    X = pd.DataFrame([{
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count,
    }])
    fare = predict(model,X)
    return {"fare": float(fare[0])}
