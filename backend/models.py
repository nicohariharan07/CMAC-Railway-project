from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from database import Base


class Train(Base):
    """Live/simulated train position and status."""
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String, unique=True, index=True)
    train_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    speed_kmph = Column(Float, default=0.0)
    status = Column(String, default="ON_TIME")  # ON_TIME | DELAYED | STOPPED
    current_station = Column(String, nullable=True)
    next_station = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)


class CrowdReading(Base):
    """Crowd density estimate for a platform/coach zone at a point in time."""
    __tablename__ = "crowd_readings"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(String, index=True)      # e.g. "PLATFORM_1", "COACH_S4"
    station_code = Column(String, index=True)
    person_count = Column(Integer)
    capacity_pct = Column(Float)              # person_count / expected capacity * 100
    source = Column(String, default="simulated_video")
    recorded_at = Column(DateTime, default=datetime.utcnow)


class SensorReading(Base):
    """Track-side / rolling-stock sensor reading (from dataset or simulator)."""
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, index=True)     # e.g. "TRACK_SEG_12", "COACH_S4_BOGIE_2"
    vibration_mm_s = Column(Float)
    temperature_c = Column(Float)
    anomaly_score = Column(Float, nullable=True)
    is_anomalous = Column(Boolean, default=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)


class DelayPrediction(Base):
    """Predicted delay for a train, produced by the ML delay model."""
    __tablename__ = "delay_predictions"

    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String, index=True)
    predicted_delay_min = Column(Float)
    weather_factor = Column(Float)
    congestion_factor = Column(Float)
    predicted_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """Unified alert feed shown on the dashboard and pushed to notification channels."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)    # CROWD | MAINTENANCE | DELAY | SAFETY
    severity = Column(String, default="MEDIUM")  # LOW | MEDIUM | HIGH | CRITICAL
    message = Column(String)
    source_ref = Column(String, nullable=True)   # train_number / zone_id / asset_id
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)
