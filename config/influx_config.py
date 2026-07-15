"""
============================================================
Project : DNS Measurement Platform
Module  : influx_config.py

Description
-----------
InfluxDB configuration.

Author
------
Helen Liu
============================================================
"""

import os


# ==========================================================
# InfluxDB Configuration
# ==========================================================

INFLUX_URL = os.getenv(
    "INFLUX_URL",
    "http://localhost:8086",
)

INFLUX_ORG = os.getenv(
    "INFLUX_ORG",
    "dns-observatory",
)

INFLUX_BUCKET = os.getenv(
    "INFLUX_BUCKET",
    "telemetry",
)

INFLUX_TOKEN = os.getenv(
    "INFLUX_TOKEN",
    "dns-observatory-token",
)