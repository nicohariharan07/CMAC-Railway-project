"""
Delay & disruption prediction module.

Trains a RandomForestRegressor on synthetic historical schedule data
(hour of day, weather severity, network congestion, trip distance) to
forecast the likely delay (in minutes) for a train. In production this
would be trained on real historical NTES/schedule data instead of the
synthetic generator below — the model interface stays identical.
"""
import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "delay_model.joblib")
_model = None


def _generate_synthetic_training_data(n_samples: int = 3000, seed: int = 7):
    rng = np.random.default_rng(seed)

    hour = rng.integers(0, 24, n_samples)
    weather = rng.uniform(0, 1, n_samples)          # 0 clear -> 1 severe
    congestion = rng.uniform(0, 1, n_samples)        # 0 empty -> 1 peak
    distance = rng.uniform(20, 1500, n_samples)      # km

    # Peak hours (8-11, 17-20) add congestion sensitivity
    peak_multiplier = np.where(
        ((hour >= 8) & (hour <= 11)) | ((hour >= 17) & (hour <= 20)), 1.6, 1.0
    )

    base_delay = (
        weather * 25
        + congestion * 20 * peak_multiplier
        + (distance / 1500) * 10
        + rng.normal(0, 4, n_samples)  # noise
    )
    delay_min = np.clip(base_delay, 0, None)

    X = np.column_stack([hour, weather, congestion, distance])
    y = delay_min
    return X, y


def train_model() -> RandomForestRegressor:
    X, y = _generate_synthetic_training_data()
    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=7)
    model.fit(X, y)
    joblib.dump(model, _MODEL_PATH)
    return model


def _get_model() -> RandomForestRegressor:
    global _model
    if _model is not None:
        return _model
    if os.path.exists(_MODEL_PATH):
        _model = joblib.load(_MODEL_PATH)
    else:
        _model = train_model()
    return _model


def predict_delay(scheduled_hour: int, weather_factor: float, congestion_factor: float, distance_km: float) -> float:
    """Returns the predicted delay in minutes for the given trip conditions."""
    model = _get_model()
    X = np.array([[scheduled_hour, weather_factor, congestion_factor, distance_km]])
    pred = float(model.predict(X)[0])
    return round(max(pred, 0.0), 1)


if __name__ == "__main__":
    train_model()
    print("Off-peak, clear weather:", predict_delay(14, 0.1, 0.2, 300))
    print("Peak hour, bad weather:", predict_delay(9, 0.8, 0.9, 300))
