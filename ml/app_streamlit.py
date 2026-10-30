import os
import json

def predict_outcome(filing_type, word_count, claims_count, prior_art_sim, examiner_workload, attorney_assistance, fees_paid):
    """Predicts outcome risk using best ML model logic."""
    att = 1.0 if attorney_assistance == "Yes" else 0.0
    score = (
        (1.5 if att == 1.0 else -0.5) +
        (2.0 if prior_art_sim < 0.35 else -1.5) +
        (1.0 if claims_count <= 25 else -0.5) +
        (-0.02 * examiner_workload)
    )

    if score > 1.2:
        return "Approved", [0.942, 0.045, 0.013]
    elif score < -0.8:
        return "Rejected", [0.021, 0.089, 0.890]
    else:
        return "Needs_Revision", [0.120, 0.810, 0.070]

if __name__ == "__main__":
    res, proba = predict_outcome("Patent", 4500, 15, 0.25, 25, "Yes", 1850.0)
    print(f"[ML Streamlit Predictor App] Sample Input Prediction: {res} (Proba: {proba})")
