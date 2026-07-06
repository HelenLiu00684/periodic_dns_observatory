"""
============================================================
Project : DNS Measurement Platform
Module  : atlas_live_collector.py

Description
-----------
Live RIPE Atlas collector.

Measurement metadata is fetched once at startup.
DNS results are fetched every 900 seconds.
Probe metadata is cached during the collector lifetime.

Author
------
Helen Liu
============================================================
"""

from __future__ import annotations
from datetime import datetime
import time
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta

import requests

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_schema import (
    create_tables,
)

from app.database.sqlite_writer import (
    save_all,
)

from app.model.observation_normalizer import (
    normalize_dns_observation,
)

from app.collector.config import (
    RAW_DIR,
    METADATA_DIR,
    PROBE_DIR,
)

from app.collector.utils import (
    save_json,
)


# ==========================================================
# Constants
# ==========================================================

RIPE_ATLAS_BASE_URL = "https://atlas.ripe.net/api/v2"

MEASUREMENT_ID = 186325158

REQUEST_TIMEOUT_SECONDS = 30

COLLECT_INTERVAL_SECONDS = 120


# ==========================================================
# Data Model
# ==========================================================

@dataclass
class CycleStats:
    """
    Statistics for one collector cycle.
    """

    cycle: int
    total_results: int = 0
    archived: int = 0
    duplicate: int = 0
    failed: int = 0
    elapsed_seconds: float = 0.0


# ==========================================================
# RIPE Atlas API
# ==========================================================

def fetch_measurement_metadata(
    measurement_id: int,
) -> Dict:
    """
    Fetch RIPE Atlas measurement metadata once.
    """

    url = (
        f"{RIPE_ATLAS_BASE_URL}"
        f"/measurements/{measurement_id}/"
    )

    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    return response.json()


def fetch_measurement_results(
    measurement_id: int,
) -> List[Dict]:
    """
    Fetch RIPE Atlas DNS measurement results.
    """

    url = (
        f"{RIPE_ATLAS_BASE_URL}"
        f"/measurements/{measurement_id}/results/"
    )

    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    return response.json()


def fetch_probe_metadata(
    probe_id: int,
) -> Dict:
    """
    Fetch RIPE Atlas probe metadata.
    """

    url = (
        f"{RIPE_ATLAS_BASE_URL}"
        f"/probes/{probe_id}/"
    )

    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Validation
# ==========================================================

def is_valid_dns_result(
    result: Dict,
) -> bool:
    """
    Check whether a RIPE Atlas result contains a usable DNS
    response packet.
    """

    if "result" not in result:
        return False

    dns_result = result["result"]

    if not isinstance(dns_result, dict):
        return False

    if not dns_result.get("abuf"):
        return False

    if result.get("prb_id") is None:
        return False

    if result.get("timestamp") is None:
        return False

    return True


# ==========================================================
# Probe Cache
# ==========================================================

def get_probe_from_cache(
    probe_id: int,
    probe_cache: Dict[int, Dict],
) -> Optional[Dict]:
    """
    Return probe metadata from cache.

    If the probe is not cached, fetch it from RIPE Atlas and
    store it in the cache.
    """

    if probe_id in probe_cache:
        return probe_cache[probe_id]

    try:
        probe = fetch_probe_metadata(
            probe_id,
        )

        save_json(
            probe,
            PROBE_DIR / f"{probe_id}.json",
        )

    except requests.RequestException as error:
        print(
            f"[WARN] Failed to fetch probe {probe_id}: {error}"
        )
        return None

    probe_cache[probe_id] = probe

    return probe


# ==========================================================
# Archive
# ==========================================================

def archive_one_result(
    connection,
    measurement: Dict,
    probe: Dict,
    result: Dict,
) -> Optional[bool]:
    """
    Normalize and archive one DNS result.

    Returns
    -------
    True
        A new Observation was inserted.

    False
        Observation already exists.

    None
        Archive operation failed.
    """

    try:
        observation = normalize_dns_observation(
            measurement,
            probe,
            result,
        )

        inserted = save_all(
            connection,
            measurement,
            probe,
            observation,
        )

        return inserted

    except Exception as error:
        print(
            "[WARN] Failed to archive result: "
            f"measurement={measurement.get('id')} "
            f"probe={result.get('prb_id')} "
            f"timestamp={result.get('timestamp')} "
            f"error={error}"
        )

        return None
    

    # ==========================================================
# Collection Cycle
# ==========================================================

def collect_once(
    connection,
    measurement: Dict,
    probe_cache: Dict[int, Dict],
    cycle_number: int,
) -> CycleStats:
    """
    Run one live collection cycle.

    Results are fetched every cycle.
    Measurement metadata is provided by caller and is not
    fetched again.
    """

    start_time = time.time()

    stats = CycleStats(
        cycle=cycle_number,
    )

    try:

        results = fetch_measurement_results(
            measurement["id"],
)

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        save_json(
            results,
            RAW_DIR / "results.json",
        )

        save_json(
            results,
            RAW_DIR / f"results_{timestamp}.json",
        )

    except requests.RequestException as error:

        print(
            f"[ERROR] Failed to fetch results: {error}"
        )

        stats.failed += 1

        stats.elapsed_seconds = (
            time.time() - start_time
        )

        return stats

    stats.total_results = len(results)

    latest_timestamp = get_latest_observation_timestamp(
        connection,
    )
    for index, result in enumerate(
        results,
        start=1,
    ):
        result_timestamp = result.get("timestamp")

        if result_timestamp is None:
            stats.failed += 1
            continue

        if result_timestamp <= latest_timestamp:
            # stats.duplicate += 1
            continue

        # --------------------------------------------------
        # Validate Result
        # --------------------------------------------------

        if not is_valid_dns_result(
            result,
        ):

            stats.failed += 1

            continue

        # --------------------------------------------------
        # Probe Metadata
        # --------------------------------------------------

        probe_id = result["prb_id"]

        probe = get_probe_from_cache(
            probe_id,
            probe_cache,
        )

        if probe is None:
            stats.failed += 1
            continue



        # --------------------------------------------------
        # Archive
        # --------------------------------------------------

        archive_result = archive_one_result(
            connection,
            measurement,
            probe,
            result,
        )

        if archive_result is True:

            stats.archived += 1

            print(
                "[INFO] Archived "
                f"#{index} "
                f"probe={probe_id} "
                f"timestamp={result.get('timestamp')}"
            )

        elif archive_result is False:

            stats.duplicate += 1

        else:

            stats.failed += 1

    stats.elapsed_seconds = (
        time.time() - start_time
    )

    return stats


# ==========================================================
# Reporting
# ==========================================================

def print_cycle_report(
    stats: CycleStats,
) -> None:
    """
    Print collector cycle statistics.
    """

    print()

    print("=" * 60)

    print(
        "DNS Measurement Platform Observatory - Live Collector"
    )

    print("=" * 60)

    print(
        f"Cycle        : {stats.cycle}"
    )

    print(
        f"Total Results: {stats.total_results}"
    )

    print(
        f"Archived     : {stats.archived}"
    )

    print(
        f"Duplicate    : {stats.duplicate}"
    )

    print(
        f"Failed       : {stats.failed}"
    )

    print(
        f"Elapsed      : {stats.elapsed_seconds:.2f} sec"
    )

    print(
        f"Next Run     : {COLLECT_INTERVAL_SECONDS} sec"
    )

    print("=" * 60)

    print()

    # ==========================================================
# Runners
# ==========================================================

def run_once() -> None:
    """
    Execute a single collection cycle.
    """

    print(
        f"[INFO] Fetching measurement metadata: {MEASUREMENT_ID}"
    )

    measurement = fetch_measurement_metadata(
        MEASUREMENT_ID,
    )

    # Save measurement metadata
    save_json(
        measurement,
        METADATA_DIR / "measurement_metadata.json",
    )
    connection = get_connection()

    probe_cache: Dict[int, Dict] = {}

    try:

        create_tables(
            connection,
        )

        stats = collect_once(
            connection,
            measurement,
            probe_cache,
            cycle_number=1,
        )

        print_cycle_report(
            stats,
        )

    finally:

        close_connection(
            connection,
        )


def run_forever() -> None:
    """
    Run the live collector continuously.

    Measurement metadata is fetched only once.

    Probe metadata is cached during the entire
    collector lifetime.

    SQLite connection is reused.
    """

    print(
        f"[INFO] Fetching measurement metadata once: {MEASUREMENT_ID}"
    )

    measurement = fetch_measurement_metadata(
        MEASUREMENT_ID,
    )

    save_json(
        measurement,
        METADATA_DIR / "measurement_metadata.json",
    )
    connection = get_connection()

    probe_cache: Dict[int, Dict] = {}

    cycle_number = 1

    next_time = datetime.now() + timedelta(
        seconds=COLLECT_INTERVAL_SECONDS
    )
    print(
    f"[INFO] Next collection: "
    f"{next_time:%Y-%m-%d %H:%M:%S}"
)

    try:

        create_tables(
            connection,
        )

        while True:

            try:

                stats = collect_once(
                    connection,
                    measurement,
                    probe_cache,
                    cycle_number,
                )

                print_cycle_report(
                    stats,
                )

            except Exception as error:

                print(
                    "[ERROR] Collector cycle failed: "
                    f"{error}"
                )

            cycle_number += 1

            print(
                f"[INFO] Sleeping "
                f"{COLLECT_INTERVAL_SECONDS} seconds..."
            )

            time.sleep(
                COLLECT_INTERVAL_SECONDS,
            )

    finally:

        close_connection(
            connection,
        )

def get_latest_observation_timestamp(connection) -> int:
    """
    Get latest observation timestamp from SQLite.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT MAX(timestamp) AS latest_timestamp
        FROM observation
        """
    )

    row = cursor.fetchone()

    if row is None:
        return 0

    latest_timestamp = row["latest_timestamp"]

    if latest_timestamp is None:
        return 0

    return int(latest_timestamp)
# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    # Run a single collection cycle.
    #
    # run_once()

    # Continuous collection.
    #


    run_forever()