from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
import config
from ml.delay_prediction import predict_delay
from alerts.notifier import send as send_alert

router = APIRouter(prefix="/api/delays", tags=["delays"])


@router.post("/predict", response_model=schemas.DelayOut)
def predict(request: schemas.DelayRequest, db: Session = Depends(get_db)):
    """Predicts delay (minutes) for a train given schedule/weather/congestion inputs."""
    predicted_min = predict_delay(
        request.scheduled_hour,
        request.weather_factor,
        request.congestion_factor,
        request.distance_km,
    )

    record = models.DelayPrediction(
        train_number=request.train_number,
        predicted_delay_min=predicted_min,
        weather_factor=request.weather_factor,
        congestion_factor=request.congestion_factor,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    if predicted_min >= config.DELAY_ALERT_THRESHOLD_MIN:
        message = f"Train {request.train_number} predicted to be delayed by {predicted_min} minutes."
        alert = models.Alert(category="DELAY", severity="MEDIUM", message=message, source_ref=request.train_number)
        db.add(alert)
        db.commit()
        send_alert(message, severity="MEDIUM")

    return record


@router.get("/recent", response_model=List[schemas.DelayOut])
def recent_predictions(limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(models.DelayPrediction)
        .order_by(models.DelayPrediction.predicted_at.desc())
        .limit(limit)
        .all()
    )
