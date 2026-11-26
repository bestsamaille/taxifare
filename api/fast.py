from fastapi import FastAPI
import os
import joblib
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="taxifare")

MODEL_PATH = os.getenv("MODEL_PATH")
model = joblib.load(MODEL_PATH)

@app.get("/")
def root():
    return {"message": "Taxifare API is running"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}

@app.get("/predict")
def predict(
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
    fare = model.predict(X)
    return {"fare": float(fare[0])}
