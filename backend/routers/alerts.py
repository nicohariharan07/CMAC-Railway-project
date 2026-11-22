from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/", response_model=List[schemas.AlertOut])
def list_alerts(limit: int = 100, unacknowledged_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(models.Alert)
    if unacknowledged_only:
        query = query.filter(models.Alert.acknowledged == False)  # noqa: E712
    return query.order_by(models.Alert.created_at.desc()).limit(limit).all()


@router.post("/{alert_id}/acknowledge", response_model=schemas.AlertOut)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    return alert
