"""
============================================================
Project : DNS Measurement Platform
Module  : telemetry_models.py

Description
-----------
Canonical Telemetry Metric Model.

This module defines the standard telemetry metric
representation used throughout the platform.

Telemetry metrics are generated from Observation objects
and may later be exported to:

    • InfluxDB
    • Prometheus
    • Kafka
    • CSV
    • Other telemetry backends

Author
------
Helen Liu
============================================================
"""

from typing import Dict


def create_empty_metric() -> Dict:
    """
    Create an empty canonical telemetry metric.

    Returns
    -------
    Dict
        Empty telemetry metric.
    """

    return {

        # Measurement name
        "measurement": "",

        # Indexed attributes
        "tags": {},

        # Numeric values
        "fields": {},

        # Unix timestamp
        "timestamp": None,
    }