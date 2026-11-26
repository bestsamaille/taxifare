"""
Classe pour les predictions
"""

import joblib
import pandas as pd

"""
model load
"""

def load_model(modelpath):
    linreg_pipeline = joblib.load(modelpath)
    return linreg_pipeline

"""
model predict
"""

def predict(model , data):
    pred = model.predict(data)
    return pred

if __name__ == "__main__":
    X_dummy = pd.DataFrame([{
          'pickup_datetime': '2013-07-06 17:18:00 UTC',
          'pickup_longitude': -73.950655,
          'pickup_latitude': 40.783282,
          'dropoff_longitude': -73.984365,
          'dropoff_latitude': 40.769802,
          'passenger_count': 1
    }])

    model = load_model("models/linreg_pipeline.joblib")

    print(predict(model, X_dummy))
