"""
============================================================
Project : DNS Measurement Platform
Module  : atlas_collector.py

Description
-----------
Coordinate the complete RIPE Atlas collection workflow.

This module collects:

• Measurement metadata

• DNS measurement results

• Probe metadata referenced by the downloaded results

All downloaded data is stored as original JSON files for
later processing by the Normalization Layer.

This module performs only collection orchestration.

Design Principle
----------------
The Collector Layer is responsible only for downloading
external data and storing the original JSON files.

No observation normalization, database operations,
telemetry generation, or analytics are performed here.

Author
------
Helen Liu
============================================================
"""

from app.collector.measurement import (
    fetch_measurement_metadata,
)

from app.collector.probes import (
    fetch_all_probes,
)

from app.collector.results import (
    fetch_results,
)


# ==========================================================
# Collection Workflow
# ==========================================================

def collect() -> list:
    """
    Execute one complete RIPE Atlas collection workflow.

    Workflow
    --------
    Download Measurement metadata

    ↓

    Download DNS measurement results

    ↓

    Extract unique Probe IDs from the results

    ↓

    Download Probe metadata

    ↓

    Store all original JSON files locally

    Returns
    -------
    list

        Raw DNS measurement results returned by RIPE Atlas.

    Engineering Note
    ----------------
    Measurement metadata and Probe metadata are saved by
    their dedicated Collector modules.

    The returned Results list may be used by another
    orchestration layer, but this function does not perform
    observation normalization or database persistence.
    """

    print("=" * 60)
    print("RIPE Atlas Collector")
    print("=" * 60)

    print(
        "\nDownloading measurement metadata..."
    )

    fetch_measurement_metadata()

    print(
        "\nDownloading measurement results..."
    )

    results = fetch_results()

    print(
        "\nDownloading probe metadata..."
    )

    fetch_all_probes(
        results,
    )

    print(
        "\nCollection completed."
    )

    return results


# ==========================================================
# Standalone Execution
# ==========================================================

if __name__ == "__main__":

    collect()