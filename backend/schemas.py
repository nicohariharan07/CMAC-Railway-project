from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrainUpdate(BaseModel):
    train_number: str
    train_name: str
    latitude: float
    longitude: float
    speed_kmph: float = 0.0
    status: str = "ON_TIME"
    current_station: Optional[str] = None
    next_station: Optional[str] = None


class TrainOut(TrainUpdate):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


class CrowdIngest(BaseModel):
    zone_id: str
    station_code: str
    # Either raw frame stats (from ml.crowd_density) or a direct count can be supplied
    person_count: int
    expected_capacity: int = 60


class CrowdOut(BaseModel):
    id: int
    zone_id: str
    station_code: str
    person_count: int
    capacity_pct: float
    source: str
    recorded_at: datetime

    class Config:
        from_attributes = True


class SensorIngest(BaseModel):
    asset_id: str
    vibration_mm_s: float
    temperature_c: float


class SensorOut(BaseModel):
    id: int
    asset_id: str
    vibration_mm_s: float
    temperature_c: float
    anomaly_score: Optional[float]
    is_anomalous: bool
    recorded_at: datetime

    class Config:
        from_attributes = True


class DelayRequest(BaseModel):
    train_number: str
    scheduled_hour: int          # 0-23, hour of day of departure
    weather_factor: float = 0.2  # 0 (clear) - 1 (severe)
    congestion_factor: float = 0.2  # 0 (empty network) - 1 (peak congestion)
    distance_km: float = 100.0


class DelayOut(BaseModel):
    id: int
    train_number: str
    predicted_delay_min: float
    weather_factor: float
    congestion_factor: float
    predicted_at: datetime

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    category: str
    severity: str
    message: str
    source_ref: Optional[str]
    created_at: datetime
    acknowledged: bool

    class Config:
        from_attributes = True
