"""
Sensor data simulator (predictive maintenance).

Generates synthetic vibration/temperature readings for a set of track
and rolling-stock assets, occasionally injecting a simulated fault, and
posts them to the CMAC API. Stands in for real IoT sensors — this project
has none.
"""
import time
import random
import requests

API_BASE = "http://localhost:8000/api/maintenance"

ASSETS = [
    "TRACK_SEG_04", "TRACK_SEG_12", "TRACK_SEG_27",
    "COACH_S4_BOGIE_2", "COACH_B2_BOGIE_1", "LOCO_WAP7_0451",
]


def generate_reading(asset_id: str, fault_probability: float = 0.04):
    """Returns a (vibration_mm_s, temperature_c) tuple, occasionally simulating a fault."""
    if random.random() < fault_probability:
        # Simulated developing fault: elevated vibration/temperature
        vibration = round(random.uniform(6.5, 10.0), 2)
        temperature = round(random.uniform(52.0, 68.0), 1)
    else:
        vibration = round(random.gauss(2.5, 0.5), 2)
        temperature = round(random.gauss(35.0, 3.5), 1)
    return max(vibration, 0.0), max(temperature, -10.0)


def run(interval_seconds: float = 4.0, cycles: int = 1000):
    print(f"[sensor_simulator] Streaming synthetic sensor data for {len(ASSETS)} assets to {API_BASE} ...")
    for _ in range(cycles):
        for asset_id in ASSETS:
            vibration, temperature = generate_reading(asset_id)
            payload = {
                "asset_id": asset_id,
                "vibration_mm_s": vibration,
                "temperature_c": temperature,
            }
            try:
                resp = requests.post(f"{API_BASE}/sensor", json=payload, timeout=5)
                resp.raise_for_status()
                flag = "ANOMALY" if resp.json().get("is_anomalous") else "normal"
                print(f"[sensor_simulator] {asset_id}: vib={vibration} temp={temperature} -> {flag}")
            except requests.RequestException as e:
                print(f"[sensor_simulator] Failed to post reading: {e}")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run()
