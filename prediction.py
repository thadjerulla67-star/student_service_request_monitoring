import json
import joblib
import pandas as pd
import streamlit as st
from pathlib import Path
from .data_processing import prepare_features

ROOT = Path(__file__).resolve().parents[1]

@st.cache_resource
def load_model():
    return joblib.load(ROOT / "models" / "trained_model.joblib")

@st.cache_data
def load_metrics():
    return json.loads((ROOT / "models" / "model_metrics.json").read_text(encoding="utf-8"))

def predict_frame(df):
    model = load_model()
    prepared = prepare_features(df)
    metrics = load_metrics()
    X = prepared[metrics["features"]].copy()
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else None
    result = prepared.copy()
    result["Predicted_SLA_Breach"] = predictions.astype(int)
    if probabilities is not None:
        result["Breach_Probability"] = probabilities
    return result

def predict_one(values):
    model = load_model()
    metrics = load_metrics()
    row = pd.DataFrame([values], columns=metrics["features"])
    prediction = int(model.predict(row)[0])
    probability = float(model.predict_proba(row)[0][1]) if hasattr(model, "predict_proba") else None
    return prediction, probability
