from fastapi import FastAPI
from pydantic import BaseModel

import tensorflow as tf
import pandas as pd
import numpy as np
import joblib
import os

from groq import Groq

# ==========================================
# LOAD MODEL
# ==========================================

model = tf.keras.models.load_model(
    "VentureCraft_Model.keras",
    compile=False
)

scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")

# ==========================================
# GROQ CLIENT
# ==========================================

api_key = os.environ.get("GROQ_API_KEY")

# ==========================================
# FASTAPI
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
# RULE ENGINE
# ==========================================

def analyze_business(data):

    kategori = data["Kategori_Bisnis"]

    analysis = []

    # ======================================
    # MODAL AWAL
    # ======================================

    if kategori == "F&B":

        if data["Modal_Awal"] < 15000000:
            analysis.append(
                "Modal awal tergolong rendah untuk bisnis F&B."
            )

        else:
            analysis.append(
                "Modal awal cukup baik untuk bisnis F&B."
            )

    elif kategori == "Retail":

        if data["Modal_Awal"] < 20000000:
            analysis.append(
                "Modal awal retail masih relatif kecil."
            )

        else:
            analysis.append(
                "Modal awal retail cukup kuat."
            )

    elif kategori == "Jasa":

        if data["Modal_Awal"] < 10000000:
            analysis.append(
                "Modal awal usaha jasa tergolong minim."
            )

        else:
            analysis.append(
                "Modal awal usaha jasa cukup stabil."
            )

    # ======================================
    # TRAFIK HARIAN
    # ======================================

    if kategori == "F&B":

        if data["Trafik_Harian"] < 40:
            analysis.append(
                "Trafik harian terlalu rendah untuk bisnis F&B."
            )

        else:
            analysis.append(
                "Trafik harian cukup baik."
            )

    elif kategori == "Retail":

        if data["Trafik_Harian"] < 25:
            analysis.append(
                "Jumlah pelanggan retail masih rendah."
            )

        else:
            analysis.append(
                "Jumlah pelanggan retail cukup baik."
            )

    elif kategori == "Jasa":

        if data["Trafik_Harian"] < 10:
            analysis.append(
                "Pelanggan jasa masih sedikit."
            )

        else:
            analysis.append(
                "Trafik pelanggan jasa cukup baik."
            )

    # ======================================
    # RASIO SEWA
    # ======================================

    if data["Rasio_Sewa_Modal"] > 0.30:

        analysis.append(
            "Rasio biaya sewa terhadap modal terlalu tinggi."
        )

    elif data["Rasio_Sewa_Modal"] > 0.20:

        analysis.append(
            "Rasio sewa cukup besar dan perlu diperhatikan."
        )

    else:

        analysis.append(
            "Rasio sewa terhadap modal masih sehat."
        )

    # ======================================
    # HARGA JUAL vs HPP
    # ======================================

    margin = (
        data["Harga_Jual"] -
        data["HPP_Per_Produk"]
    )

    margin_ratio = margin / data["Harga_Jual"]

    if margin_ratio < 0.30:

        analysis.append(
            "Margin keuntungan produk terlalu kecil."
        )

    elif margin_ratio < 0.50:

        analysis.append(
            "Margin keuntungan cukup baik."
        )

    else:

        analysis.append(
            "Margin keuntungan sangat baik."
        )

    return analysis

# ==========================================
# LLM RESPONSE
# ==========================================

import json

def generate_llm_response(
    prediction,
    confidence,
    analysis,
    data
):

    prompt = f"""
Anda adalah konsultan bisnis profesional.

Data bisnis:
{data}

Prediksi model:
- Prediksi: {prediction}
- Confidence: {confidence:.2f}

Analisis fitur:
{analysis}

Buat output JSON VALID dengan format:

{{
  "professional_review": "...",

  "strengths": [
    "...",
    "..."
  ],

  "weaknesses": [
    "...",
    "..."
  ],

  "recommendations": [
    "...",
    "..."
  ],

  "final_summary": "..."
}}

Aturan:
- Gunakan bahasa Indonesia
- Jangan gunakan markdown
- Jangan gunakan ```json
- Output HARUS valid JSON
"""

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,
        max_tokens=700
    )

    response_text = (
        completion
        .choices[0]
        .message
        .content
    )

    try:

        parsed_json = json.loads(
            response_text
        )

        return parsed_json

    except:

        return {
            "professional_review": response_text,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "final_summary": response_text
        }

# ==========================================
# PREDICT ENDPOINT
# ==========================================

@app.post("/predict")

def predict(data: BusinessInput):

    # ======================================
    # DATAFRAME
    # ======================================

    df = pd.DataFrame([data.dict()])

    numeric_cols = [
        'Modal_Awal',
        'Biaya_Sewa_Bulan',
        'Biaya_Operasional_Bulan',
        'HPP_Per_Produk',
        'Harga_Jual',
        'Trafik_Harian',
        'Rasio_Sewa_Modal',
    ]

    # ======================================
    # ENCODING
    # ======================================

    kat_encoded = encoder.transform(
        df[['Kategori_Bisnis']]
    )

    num_features = df[numeric_cols].values

    final_features = np.hstack([
        num_features,
        kat_encoded
    ])

    final_features_scaled = scaler.transform(
        final_features
    )

    # ======================================
    # PREDICTION
    # ======================================

    prediction_prob = model.predict(
        final_features_scaled,
        verbose=0
    )[0][0]

    prediction_status = (
        "SUKSES"
        if prediction_prob > 0.5
        else "RISIKO BANGKRUT"
    )

    # ======================================
    # RULE ENGINE
    # ======================================

    analysis = analyze_business(
        data.dict()
    )

    # ======================================
    # LLM
    # ======================================

    llm_response = generate_llm_response(
        prediction_status,
        prediction_prob,
        analysis,
        data.dict()
    )

    # ======================================
    # RESPONSE
    # ======================================

    return {

      "prediction": prediction_status,

      "confidence_score": float(
          prediction_prob
      ),

      "feature_analysis": analysis,

      "professional_review":
          llm_response.get(
              "professional_review"
          ),

      "strengths":
          llm_response.get(
              "strengths"
          ),

      "weaknesses":
          llm_response.get(
              "weaknesses"
          ),

      "recommendations":
          llm_response.get(
              "recommendations"
          ),

      "final_summary":
          llm_response.get(
              "final_summary"
          )
    }
