"""
============================================================
Project : DNS Measurement Platform
Module  : measurement.py

Description
-----------
Collect RIPE Atlas Measurement metadata.

This module downloads Measurement metadata from the RIPE
Atlas REST API and stores the raw JSON locally.

The downloaded metadata is preserved without modification
for later processing by the Normalization Layer.

This module performs only data collection.

Design Principle
----------------
Collector modules are responsible only for downloading
external data and storing the original JSON files.

No business logic, observation normalization, archive
operations, or telemetry generation should occur here.

Author
------
Helen Liu
============================================================
"""

from config.collector_config import (
    BASE_URL,
    MEASUREMENT_ID,
    METADATA_DIR,
)

from app.common.json_utils import (
    download_json,
    save_json,
)


# ==========================================================
# Measurement Collection
# ==========================================================

def fetch_measurement_metadata() -> dict:
    """
    Download RIPE Atlas Measurement metadata.

    Returns
    -------
    dict

        Raw Measurement metadata returned by the
        RIPE Atlas REST API.

    Engineering Note
    ----------------
    The downloaded JSON is stored without modification.

    Observation normalization is performed later by the
    Normalization Layer.

    This module does not perform:

    • Observation construction

    • SQLite archive operations

    • Telemetry generation
    """

    url = (
        f"{BASE_URL}"
        f"/measurements/{MEASUREMENT_ID}/"
    )

    measurement = download_json(
        url,
    )

    save_json(
        measurement,
        METADATA_DIR
        / "measurement_metadata.json",
    )

    return measurement


# ==========================================================
# Standalone Verification
# ==========================================================

if __name__ == "__main__":

    measurement = fetch_measurement_metadata()

    print(
        f"Measurement ID: "
        f"{measurement['id']}"
        
    )