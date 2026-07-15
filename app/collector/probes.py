"""
============================================================
Project : DNS Measurement Platform
Module  : probes.py

Description
-----------
Collect RIPE Atlas Probe metadata.

This module downloads metadata for individual RIPE Atlas
Probes and stores the original JSON files locally.

Probe metadata is collected based on the Probe IDs found
in downloaded DNS measurement results.

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
    PROBE_DIR,
)

from app.common.json_utils import (
    download_json,
    save_json,
)


# ==========================================================
# Probe Collection
# ==========================================================

def fetch_probe(
    probe_id: int,
) -> dict:
    """
    Download metadata for a single RIPE Atlas Probe.

    Parameters
    ----------
    probe_id : int

        RIPE Atlas Probe ID.

    Returns
    -------
    dict

        Raw Probe metadata returned by the
        RIPE Atlas REST API.

    Engineering Note
    ----------------
    The downloaded JSON is stored without modification.

    This module does not perform:

    • Observation normalization

    • SQLite archive operations

    • Telemetry generation
    """

    url = (
        f"{BASE_URL}"
        f"/probes/{probe_id}/"
    )

    probe = download_json(
        url,
    )

    save_json(
        probe,
        PROBE_DIR / f"{probe_id}.json",
    )

    return probe


# ==========================================================
# Batch Probe Collection
# ==========================================================

def fetch_all_probes(
    results: list,
) -> None:
    """
    Download metadata for all unique Probes appearing in
    a collection of DNS measurement results.

    Parameters
    ----------
    results : list

        Raw DNS measurement results downloaded from
        RIPE Atlas.

    Engineering Note
    ----------------
    The RIPE Atlas Results API returns Probe IDs together
    with DNS observations.

    Probe metadata is therefore collected after downloading
    measurement results.

    Each unique Probe is downloaded exactly once.

    Duplicate Probe IDs are removed before downloading.

    Each Probe is collected only once, even if multiple
    DNS observations originate from the same Probe.

    Collection continues even if an individual Probe
    cannot be downloaded.
    """

    probe_ids = sorted(
        {
            result["prb_id"]
            for result in results
            if "prb_id" in result
        }
    )

    print(
        f"Found {len(probe_ids)} unique Probes."
    )

    for probe_id in probe_ids:

        try:

            fetch_probe(
                probe_id,
            )

        except Exception as error:

            print(
                f"Failed to download Probe "
                f"{probe_id}: {error}"
            )