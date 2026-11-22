"""
Runs all CMAC simulators concurrently (train movement, sensors, crowd data).

Usage:
    python simulator/run_simulator.py

Make sure the backend API is already running (uvicorn main:app) before
starting this script.
"""
import threading

from simulator import train_simulator, sensor_simulator, crowd_simulator


def main():
    threads = [
        threading.Thread(target=train_simulator.run, daemon=True),
        threading.Thread(target=sensor_simulator.run, daemon=True),
        threading.Thread(target=crowd_simulator.run, daemon=True),
    ]
    for t in threads:
        t.start()

    print("[run_simulator] All simulators running. Press Ctrl+C to stop.")
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n[run_simulator] Stopped.")


if __name__ == "__main__":
    main()
