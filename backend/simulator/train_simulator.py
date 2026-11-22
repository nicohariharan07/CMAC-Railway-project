"""
Train movement simulator.

Generates realistic train GPS positions moving along fixed routes and
pushes them to the CMAC API, standing in for a public GPS/schedule API
feed. Pure software — no GPS hardware involved.
"""
import time
import random
import requests

API_BASE = "http://localhost:8000/api/trains"

# A handful of illustrative routes: (train_number, name, [(lat, lon, station_name), ...])
ROUTES = [
    ("12621", "Tamil Nadu Express", [
        (13.0827, 80.2707, "Chennai Central"),
        (12.9165, 79.1325, "Katpadi"),
        (12.2958, 76.6394, "Jolarpettai"),
        (13.3524, 78.1287, "Bangarapet"),
    ]),
    ("12639", "Brindavan Express", [
        (13.0827, 80.2707, "Chennai Central"),
        (12.8342, 79.7036, "Arakkonam"),
        (12.5266, 78.2150, "Vellore"),
        (12.9716, 77.5946, "Bangalore City"),
    ]),
    ("22625", "Chennai-Bengaluru SF", [
        (13.0827, 80.2707, "Chennai Central"),
        (13.0389, 79.6008, "Tiruvallur"),
        (12.6389, 78.5678, "Krishnagiri"),
        (12.9716, 77.5946, "Bangalore City"),
    ]),
]


def interpolate(p1, p2, fraction):
    lat = p1[0] + (p2[0] - p1[0]) * fraction
    lon = p1[1] + (p2[1] - p1[1]) * fraction
    return lat, lon


def simulate_route(train_number, name, waypoints, steps_per_leg=8):
    """Yields simulated position updates moving smoothly along the route."""
    for i in range(len(waypoints) - 1):
        start = waypoints[i]
        end = waypoints[i + 1]
        for step in range(steps_per_leg):
            fraction = step / steps_per_leg
            lat, lon = interpolate(start, end, fraction)
            speed = round(random.uniform(60, 120), 1)
            status = random.choices(["ON_TIME", "DELAYED"], weights=[0.85, 0.15])[0]
            yield {
                "train_number": train_number,
                "train_name": name,
                "latitude": round(lat, 5),
                "longitude": round(lon, 5),
                "speed_kmph": speed,
                "status": status,
                "current_station": start[2],
                "next_station": end[2],
            }


def run(interval_seconds: float = 3.0, cycles: int = 1000):
    """Continuously posts simulated positions for every route, round-robin."""
    generators = {
        t[0]: simulate_route(*t) for t in ROUTES
    }
    print(f"[train_simulator] Streaming {len(ROUTES)} simulated trains to {API_BASE} ...")

    for _ in range(cycles):
        for train_number, gen in list(generators.items()):
            try:
                update = next(gen)
            except StopIteration:
                # restart the route once it reaches the end
                route = next(t for t in ROUTES if t[0] == train_number)
                generators[train_number] = simulate_route(*route)
                update = next(generators[train_number])

            try:
                resp = requests.post(f"{API_BASE}/update", json=update, timeout=5)
                resp.raise_for_status()
                print(f"[train_simulator] {update['train_number']} -> {update['current_station']} -> {update['next_station']}")
            except requests.RequestException as e:
                print(f"[train_simulator] Failed to post update: {e}")

        time.sleep(interval_seconds)


if __name__ == "__main__":
    run()
