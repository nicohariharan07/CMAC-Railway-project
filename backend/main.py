"""
CMAC - Centralized Monitoring, Analytics & Control
FastAPI backend entrypoint.

Run locally with:
    uvicorn main:app --reload --port 8000

This is a fully software system: every "live" data point in this API is
sourced from public datasets/APIs or the simulator scripts in
backend/simulator/ — no physical device ever talks to this server.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models  # noqa: F401 (ensures models are registered before create_all)
from routers import trains, crowd, maintenance, delays, alerts
import config

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CMAC - Centralized Monitoring, Analytics & Control",
    description="AI-powered, fully software railway management platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_ORIGIN, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trains.router)
app.include_router(crowd.router)
app.include_router(maintenance.router)
app.include_router(delays.router)
app.include_router(alerts.router)


@app.get("/")
def root():
    return {
        "project": "CMAC",
        "status": "running",
        "docs": "/docs",
        "note": "Fully software system — all data is simulated or sourced from public datasets/APIs.",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
