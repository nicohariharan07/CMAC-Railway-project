"""
Predictive maintenance module.

Trains an IsolationForest anomaly-detection model on synthetic (or, once
available, publicly published) vibration/temperature sensor data, then
scores new readings so at-risk track/rolling-stock assets can be flagged
before they actually fail. Pure software — no physical sensors required;
data comes from ml/../simulator/sensor_simulator.py or a downloaded dataset.
"""
import os
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "maintenance_model.joblib")
_model = None


def _generate_synthetic_training_data(n_normal: int = 2000, n_anomalous: int = 60, seed: int = 42):
    """
    Generates a realistic synthetic training set:
    - Normal operation: vibration ~ N(2.5, 0.6) mm/s, temperature ~ N(35, 4) C
    - Anomalous (worn bearing / overheating): higher vibration and/or temperature
    """
    rng = np.random.default_rng(seed)
    normal_vibration = rng.normal(2.5, 0.6, n_normal)
    normal_temp = rng.normal(35.0, 4.0, n_normal)
    normal = np.column_stack([normal_vibration, normal_temp])

    anomalous_vibration = rng.normal(7.5, 1.5, n_anomalous)
    anomalous_temp = rng.normal(58.0, 6.0, n_anomalous)
    anomalous = np.column_stack([anomalous_vibration, anomalous_temp])

    X = np.vstack([normal, anomalous])
    return X


def train_model() -> IsolationForest:
    """Trains (or retrains) the IsolationForest model and persists it to disk."""
    X = _generate_synthetic_training_data()
    model = IsolationForest(
        n_estimators=200,
        contamination=0.03,
        random_state=42,
    )
    model.fit(X)
    joblib.dump(model, _MODEL_PATH)
    return model


def _get_model() -> IsolationForest:
    global _model
    if _model is not None:
        return _model
    if os.path.exists(_MODEL_PATH):
        _model = joblib.load(_MODEL_PATH)
    else:
        _model = train_model()
    return _model


def score_reading(vibration_mm_s: float, temperature_c: float):
    """
    Returns (anomaly_score, is_anomalous) for a single sensor reading.
    Lower anomaly_score = more anomalous (IsolationForest convention).
    """
    model = _get_model()
    X = np.array([[vibration_mm_s, temperature_c]])
    score = float(model.decision_function(X)[0])
    is_anomalous = bool(model.predict(X)[0] == -1)
    return score, is_anomalous


if __name__ == "__main__":
    # Run directly to (re)train and sanity-check the model
    train_model()
    print("Normal reading:", score_reading(2.4, 34.0))
    print("Anomalous reading:", score_reading(8.9, 61.0))
