from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
import config
from ml.predictive_maintenance import score_reading
from alerts.notifier import send as send_alert

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])


@router.post("/sensor", response_model=schemas.SensorOut)
def ingest_sensor_reading(reading: schemas.SensorIngest, db: Session = Depends(get_db)):
    """
    Records a sensor reading and scores it with the IsolationForest anomaly
    model. `reading` comes from simulator/sensor_simulator.py or a public
    dataset — no physical sensor hardware involved.
    """
    score, is_anomalous = score_reading(reading.vibration_mm_s, reading.temperature_c)

    record = models.SensorReading(
        asset_id=reading.asset_id,
        vibration_mm_s=reading.vibration_mm_s,
        temperature_c=reading.temperature_c,
        anomaly_score=score,
        is_anomalous=is_anomalous,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    if is_anomalous or score <= config.MAINTENANCE_ANOMALY_THRESHOLD:
        message = (
            f"Predictive maintenance alert on {reading.asset_id}: "
            f"vibration={reading.vibration_mm_s}mm/s, temp={reading.temperature_c}C "
            f"(anomaly score {round(score, 3)})."
        )
        alert = models.Alert(category="MAINTENANCE", severity="CRITICAL", message=message, source_ref=reading.asset_id)
        db.add(alert)
        db.commit()
        send_alert(message, severity="CRITICAL")

    return record


@router.get("/readings", response_model=List[schemas.SensorOut])
def latest_readings(limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(models.SensorReading)
        .order_by(models.SensorReading.recorded_at.desc())
        .limit(limit)
        .all()
    )
