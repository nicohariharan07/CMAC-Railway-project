from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
import config
from ml.crowd_density import estimate_capacity_pct
from alerts.notifier import send as send_alert

router = APIRouter(prefix="/api/crowd", tags=["crowd"])


@router.post("/ingest", response_model=schemas.CrowdOut)
def ingest_crowd_reading(reading: schemas.CrowdIngest, db: Session = Depends(get_db)):
    """
    Records a crowd density reading. `person_count` is produced upstream by
    ml.crowd_density.count_people_in_frame() run against a sample/public
    video dataset or the crowd simulator — never a live camera feed.
    Automatically raises an alert if capacity is exceeded.
    """
    capacity_pct = estimate_capacity_pct(reading.person_count, reading.expected_capacity)

    record = models.CrowdReading(
        zone_id=reading.zone_id,
        station_code=reading.station_code,
        person_count=reading.person_count,
        capacity_pct=capacity_pct,
        source="simulated_video",
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    if reading.person_count >= config.CROWD_ALERT_THRESHOLD:
        message = (
            f"Overcrowding detected at {reading.zone_id} ({reading.station_code}): "
            f"{reading.person_count} people ({capacity_pct}% of capacity)."
        )
        alert = models.Alert(category="CROWD", severity="HIGH", message=message, source_ref=reading.zone_id)
        db.add(alert)
        db.commit()
        send_alert(message, severity="HIGH")

    return record


@router.get("/latest", response_model=List[schemas.CrowdOut])
def latest_readings(limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(models.CrowdReading)
        .order_by(models.CrowdReading.recorded_at.desc())
        .limit(limit)
        .all()
    )
