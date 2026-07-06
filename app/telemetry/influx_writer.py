"""
============================================================
Project : DNS Measurement Platform
Module  : influx_writer.py

Description
-----------
Write Telemetry Metrics into InfluxDB.

Responsibilities
----------------
✓ Convert Canonical Telemetry Metrics

✓ Write Metrics into InfluxDB

This module does NOT

✗ Read SQLite

✗ Build Metrics

✗ Parse DNS

Author
------
Helen Liu
============================================================
"""

from typing import Dict, List

from influxdb_client import (
    InfluxDBClient,
    Point,
    WritePrecision,
)

from influxdb_client.client.write_api import (
    SYNCHRONOUS,
)


# ==========================================================
# Configuration
# ==========================================================

INFLUX_URL = "http://localhost:8086"

INFLUX_TOKEN = "YOUR_TOKEN"

INFLUX_ORG = "YOUR_ORG"

INFLUX_BUCKET = "dns_observatory"


# ==========================================================
# Client
# ==========================================================

def create_client() -> InfluxDBClient:
    """
    Create an InfluxDB client.
    """

    return InfluxDBClient(

        url=INFLUX_URL,

        token=INFLUX_TOKEN,

        org=INFLUX_ORG,
    )


# ==========================================================
# Build Point
# ==========================================================

def _build_point(
    metric: Dict,
) -> Point:
    """
    Convert one Canonical Telemetry Metric into an InfluxDB Point.
    """

    point = Point(
        metric["measurement"]
    )

    #
    # Tags
    #

    for key, value in metric["tags"].items():

        point.tag(
            key,
            str(value),
        )

    #
    # Fields
    #

    for key, value in metric["fields"].items():

        point.field(
            key,
            value,
        )

    #
    # Timestamp
    #

    point.time(

        metric["timestamp"],

        WritePrecision.S,
    )

    return point


# ==========================================================
# Public API
# ==========================================================

def write_metrics(
    metrics: List[Dict],
) -> int:
    """
    Write Telemetry Metrics into InfluxDB.

    Returns
    -------
    int
        Number of written metrics.
    """

    if not metrics:

        return 0

    client = create_client()

    write_api = client.write_api(
        write_options=SYNCHRONOUS,
    )

    points = []

    for metric in metrics:

        points.append(

            _build_point(
                metric,
            )

        )

    write_api.write(

        bucket=INFLUX_BUCKET,

        record=points,
    )

    client.close()

    return len(points)