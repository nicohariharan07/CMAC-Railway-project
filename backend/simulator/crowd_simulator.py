"""
Crowd data simulator.

Generates synthetic platform/coach footfall counts with realistic peak-hour
patterns and posts them to the CMAC API. This stands in for running
ml.crowd_density.count_people_in_frame() against a public/sample video
dataset — useful for demoing the full pipeline without needing to source
and download video files first.
"""
import time
import random
import datetime
import requests

API_BASE = "http://localhost:8000/api/crowd"

ZONES = [
    ("PLATFORM_1", "MAS", 80),
    ("PLATFORM_2", "MAS", 80),
    ("PLATFORM_5", "MAS", 100),
    ("COACH_S4", "MAS", 72),
    ("PLATFORM_1", "AJJ", 60),
]


def _peak_multiplier():
    hour = datetime.datetime.now().hour
    if hour in (8, 9, 18, 19):
        return random.uniform(1.4, 1.9)
    if hour in (7, 10, 17, 20):
        return random.uniform(1.1, 1.4)
    return random.uniform(0.4, 0.9)


def run(interval_seconds: float = 5.0, cycles: int = 1000):
    print(f"[crowd_simulator] Streaming synthetic crowd data for {len(ZONES)} zones to {API_BASE} ...")
    for _ in range(cycles):
        for zone_id, station_code, capacity in ZONES:
            base = capacity * 0.35
            count = int(max(0, random.gauss(base, capacity * 0.15) * _peak_multiplier()))
            payload = {
                "zone_id": zone_id,
                "station_code": station_code,
                "person_count": count,
                "expected_capacity": capacity,
            }
            try:
                resp = requests.post(f"{API_BASE}/ingest", json=payload, timeout=5)
                resp.raise_for_status()
                pct = resp.json().get("capacity_pct")
                print(f"[crowd_simulator] {station_code}/{zone_id}: {count} people ({pct}% capacity)")
            except requests.RequestException as e:
                print(f"[crowd_simulator] Failed to post reading: {e}")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run()
