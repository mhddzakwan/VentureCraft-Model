from fastapi import FastAPI
from pydantic import BaseModel

import tensorflow as tf
import pandas as pd
import numpy as np
import joblib

# ==========================================
# LOAD MODEL & PREPROCESSOR
# ==========================================

model = tf.keras.models.load_model(
    "VentureCraft_Model.keras",
    compile=False
)

scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")

# ==========================================
# FASTAPI INIT
# ==========================================

app = FastAPI()

# ==========================================
# INPUT SCHEMA
# ==========================================

class BusinessInput(BaseModel):

    Kategori_Bisnis: str
    Modal_Awal: float
    Biaya_Sewa_Bulan: float
    Biaya_Operasional_Bulan: float
    HPP_Per_Produk: float
    Harga_Jual: float
    Trafik_Harian: float
    Rasio_Sewa_Modal: float

# ==========================================
# PREDICT ENDPOINT
# ==========================================

@app.post("/predict")

def predict(data: BusinessInput):

    # Convert ke dataframe
    df = pd.DataFrame([data.dict()])

    # Numeric columns
    numeric_cols = [
        'Modal_Awal',
        'Biaya_Sewa_Bulan',
        'Biaya_Operasional_Bulan',
        'HPP_Per_Produk',
        'Harga_Jual',
        'Trafik_Harian',
        'Rasio_Sewa_Modal',
    ]

    # One-hot encoding
    kat_encoded = encoder.transform(
        df[['Kategori_Bisnis']]
    )

    # Numeric features
    num_features = df[numeric_cols].values

    # Combine
    final_features = np.hstack([
        num_features,
        kat_encoded
    ])

    # Scaling
    final_features_scaled = scaler.transform(final_features)

    # Predict
    prediction_prob = model.predict(
        final_features_scaled,
        verbose=0
    )[0][0]

    # Threshold
    prediction_status = (
        "SUKSES"
        if prediction_prob > 0.5
        else "RISIKO BANGKRUT"
    )

    return {
        "prediction": prediction_status,
        "confidence_score": float(prediction_prob)
    }