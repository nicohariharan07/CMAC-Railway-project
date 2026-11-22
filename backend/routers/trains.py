from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/trains", tags=["trains"])


@router.get("/", response_model=List[schemas.TrainOut])
def list_trains(db: Session = Depends(get_db)):
    """Returns the latest known position/status for every tracked train."""
    return db.query(models.Train).order_by(models.Train.updated_at.desc()).all()


@router.get("/{train_number}", response_model=schemas.TrainOut)
def get_train(train_number: str, db: Session = Depends(get_db)):
    return db.query(models.Train).filter(models.Train.train_number == train_number).first()


@router.post("/update", response_model=schemas.TrainOut)
def update_train(update: schemas.TrainUpdate, db: Session = Depends(get_db)):
    """
    Upserts a train's position/status. Called by the train simulator
    (or, in production, by a public schedule/GPS API poller) — never by
    physical trackside hardware directly.
    """
    train = db.query(models.Train).filter(models.Train.train_number == update.train_number).first()
    if train is None:
        train = models.Train(**update.model_dump())
        db.add(train)
    else:
        for field, value in update.model_dump().items():
            setattr(train, field, value)
        train.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(train)
    return train
