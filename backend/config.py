"""
CMAC - Central configuration.
All settings are read from environment variables with sensible local defaults,
so the whole stack runs on a laptop with zero physical hardware.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Default to local SQLite for a zero-setup dev run.
# Swap to Postgres/TimescaleDB in production via DATABASE_URL, e.g.:
#   postgresql://cmac:cmac@localhost:5432/cmac
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cmac.db")

# Crowd density alert threshold (people count per platform zone)
CROWD_ALERT_THRESHOLD = int(os.getenv("CROWD_ALERT_THRESHOLD", "40"))

# Predictive maintenance anomaly score threshold (IsolationForest, lower = more anomalous)
MAINTENANCE_ANOMALY_THRESHOLD = float(os.getenv("MAINTENANCE_ANOMALY_THRESHOLD", "-0.15"))

# Delay prediction alert threshold (minutes)
DELAY_ALERT_THRESHOLD_MIN = int(os.getenv("DELAY_ALERT_THRESHOLD_MIN", "15"))

# Notification channel toggles (all default to "console" — safe with no API keys)
NOTIFY_CHANNEL = os.getenv("NOTIFY_CHANNEL", "console")  # console | twilio | whatsapp
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
ALERT_TO_NUMBER = os.getenv("ALERT_TO_NUMBER", "")

# CORS
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
