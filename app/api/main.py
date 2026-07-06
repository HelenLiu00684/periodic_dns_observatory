"""
============================================================
Project : DNS Measurement Platform
Module  : main.py

Description
-----------
FastAPI application entry point.

Author
------
Helen Liu
============================================================
"""

from fastapi import FastAPI

from app.api.routes.health import router as health_router

from app.api.routes.statistics import router as statistics_router

from app.api.routes.measurement import router as measurement_router
from app.api.routes.measurements import router as measurements_router

from app.api.routes.probe import router as probe_router
from app.api.routes.probes import router as probes_router

from app.api.routes.observation import router as observation_router
from app.api.routes.observations import router as observations_router

app = FastAPI(
    title="DNS Measurement Platform",
    version="1.0.0",
    description="DNS Measurement Platform REST API"
)

app.include_router(health_router)

app.include_router(statistics_router)
app.include_router(measurements_router)
app.include_router(measurement_router)
app.include_router(probes_router)
app.include_router(probe_router)
app.include_router(observations_router)
app.include_router(observation_router)

@app.get("/", tags=["System"])
def root():
    """
    Root endpoint.
    """

    return {
        "project": "DNS Measurement Platform",
        "version": "1.0.0",
        "status": "running"
    }