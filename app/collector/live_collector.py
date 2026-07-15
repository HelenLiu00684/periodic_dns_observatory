"""
============================================================
Project : DNS Measurement Platform
Module  : live_collector.py

Description
-----------
Live RIPE Atlas Collector.

This module periodically collects DNS measurement data from
the RIPE Atlas REST API.

Collected data includes:

• Measurement metadata

• DNS measurement results

• Probe metadata

All downloaded data is stored as original JSON files for
later processing.

This module performs only data collection.

Design Principle
----------------
The Collector Layer is responsible only for collecting
external data.

No observation normalization, database operations,
telemetry generation, or analytics are performed here.

Author
------
Helen Liu
============================================================
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Dict

from app.collector.measurement import (
    fetch_measurement_metadata,
)

from app.collector.results import (
    fetch_results,
)

from app.collector.probes import (
    fetch_all_probes,
)

from config.collector_config import (
    COLLECT_INTERVAL_SECONDS,
)


# ==========================================================
# Collection Cycle
# ==========================================================

def collect_once() -> list:
    """
    Execute one complete collection cycle.

    Workflow
    --------
    Download Measurement metadata

    ↓

    Download DNS measurement results

    ↓

    Download Probe metadata

    ↓

    Store original JSON files

    Returns
    -------
    list

        Raw DNS measurement results.

    Engineering Note
    ----------------
    This function performs only collection.

    No observation normalization or archive operations
    occur here.
    """

    print("=" * 60)
    print("RIPE Atlas Live Collector")
    print("=" * 60)

    print(
        "\nDownloading measurement metadata..."
    )

    fetch_measurement_metadata()

    print(
        "\nDownloading DNS results..."
    )

    results = fetch_results()

    print(
        "\nDownloading Probe metadata..."
    )

    fetch_all_probes(
        results,
    )

    print(
        "\nCollection cycle completed."
    )

    return results


# ==========================================================
# Continuous Collection
# ==========================================================

def run_forever() -> None:
    """
    Run the Collector continuously.

    Measurement metadata, DNS results, and Probe metadata
    are collected periodically.

    Engineering Note
    ----------------
    The Collector Layer stores only raw JSON files.

    Subsequent processing is handled by the
    Normalization Layer.
    """

    cycle = 1

    while True:

        print()

        print("=" * 60)

        print(
            f"Collection Cycle {cycle}"
        )

        print("=" * 60)

        start_time = datetime.now()

        collect_once()

        elapsed = (
            datetime.now()
            - start_time
        ).total_seconds()

        print()

        print(
            f"Elapsed : {elapsed:.2f} sec"
        )

        print(
            f"Sleeping: "
            f"{COLLECT_INTERVAL_SECONDS} sec"
        )

        cycle += 1

        time.sleep(
            COLLECT_INTERVAL_SECONDS,
        )


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    run_forever()