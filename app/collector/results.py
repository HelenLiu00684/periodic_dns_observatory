"""
============================================================
Project : DNS Measurement Platform
Module  : results.py

Description
-----------
Collect RIPE Atlas DNS measurement results.

This module downloads raw DNS measurement results from the
RIPE Atlas REST API and stores the original JSON locally.

The downloaded results are preserved without modification
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
    RAW_DIR,
)

from app.common.json_utils import (
    download_json,
    save_json,
)


# ==========================================================
# Results Collection
# ==========================================================

def fetch_results() -> list:
    """
    Download RIPE Atlas DNS measurement results.

    Returns
    -------
    list

        Raw DNS measurement results returned by the
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
        f"/measurements/{MEASUREMENT_ID}/results/"
    )

    results = download_json(
        url,
    )

    save_json(
        results,
        RAW_DIR / "results.json",
    )

    return results


# ==========================================================
# Standalone Verification
# ==========================================================

if __name__ == "__main__":

    results = fetch_results()

    print(
        f"Downloaded {len(results)} DNS results."
    )