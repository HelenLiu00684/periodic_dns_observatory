"""
============================================================
Project : West Africa DNS Observatory
Module  : test_archive_pipeline.py

Description
-----------
Integration test for the complete SQLite archive pipeline
using REAL RIPE Atlas data collected by the Collector.
============================================================
"""

import json
from pathlib import Path

from app.model.observation_normalizer import (
    normalize_dns_observation,
)

from app.database.sqlite_writer import (
    save_all,
)

from app.database.sqlite_reader import (
    get_measurement,
    get_probe,
    get_observation,
)


def test_archive_pipeline(db_connection):
    """
    Verify the complete archive pipeline:

    Measurement Metadata
        + Probe Metadata
        + DNS Result
        -> Observation Normalizer
        -> SQLite Writer
        -> SQLite Reader
    """

    # ======================================================
    # Load real Collector data
    # ======================================================

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"

    with open(
        data_dir / "metadata" / "measurement_metadata.json",
        "r",
        encoding="utf-8",
    ) as f:
        measurement = json.load(f)

    with open(
        data_dir / "raw" / "results.json",
        "r",
        encoding="utf-8",
    ) as f:
        results = json.load(f)

    # ======================================================
    # Select one usable DNS result
    #
    # Requirements:
    #   - has DNS result section
    #   - has abuf DNS packet
    #   - has a matching probe metadata file
    # ======================================================

    selected_result = None
    probe = None

    for item in results:

        if "result" not in item:
            continue

        if "abuf" not in item["result"]:
            continue

        probe_id = item.get("prb_id")

        if probe_id is None:
            continue

        probe_path = data_dir / "probes" / f"{probe_id}.json"

        if not probe_path.exists():
            continue

        with open(
            probe_path,
            "r",
            encoding="utf-8",
        ) as f:
            probe = json.load(f)

        selected_result = item
        break

    assert selected_result is not None
    assert probe is not None

    # ======================================================
    # Normalize
    # ======================================================

    observation = normalize_dns_observation(
        measurement,
        probe,
        selected_result,
    )

    # ======================================================
    # Save into SQLite Archive
    # ======================================================

    save_all(
        db_connection,
        measurement,
        probe,
        observation,
    )

    # save_all() already commits internally.

    # ======================================================
    # Read back from SQLite Archive
    # ======================================================

    measurement_db = get_measurement(
        db_connection,
        measurement["id"],
    )

    probe_db = get_probe(
        db_connection,
        probe["id"],
    )

    observation_db = get_observation(
        db_connection,
        observation["identity"]["observation_id"],
    )

    # ======================================================
    # Assert Measurement
    # ======================================================

    assert measurement_db is not None

    assert measurement_db["measurement_id"] == measurement["id"]
    assert measurement_db["description"] == measurement["description"]
    assert measurement_db["target"] == measurement["target"]
    assert measurement_db["interval_seconds"] == measurement["interval"]
    assert measurement_db["protocol"] == measurement["type"]
    assert measurement_db["address_family"] == measurement["af"]

    # ======================================================
    # Assert Probe
    # ======================================================

    assert probe_db is not None

    assert probe_db["probe_id"] == probe["id"]
    assert probe_db["asn_v4"] == probe.get("asn_v4")
    assert probe_db["country_code"] == probe.get("country_code")
    assert probe_db["description"] == probe.get("description")

    # ======================================================
    # Assert Observation
    # ======================================================

    assert observation_db is not None

    assert (
        observation_db["observation_id"]
        == observation["identity"]["observation_id"]
    )

    assert (
        observation_db["identity"]["measurement_id"]
        == measurement["id"]
    )

    assert (
        observation_db["identity"]["probe_id"]
        == probe["id"]
    )

    assert (
        observation_db["metadata"]["timestamp"]
        == selected_result["timestamp"]
    )

    assert (
        observation_db["metadata"]["stored_timestamp"]
        == selected_result["stored_timestamp"]
    )

    assert (
        observation_db["metadata"]["observation_type"]
        == "DNS"
    )

    assert (
        observation_db["network"]["resolver_ip"]
        == selected_result["dst_addr"]
    )

    assert (
        observation_db["network"]["destination_port"]
        == int(selected_result["dst_port"])
    )

    assert (
        observation_db["network"]["transport_protocol"]
        == selected_result["proto"]
    )

    assert (
        observation_db["network"]["response_time"]
        == selected_result["result"]["rt"]
    )

    assert (
        observation_db["protocol"]["raw_abuf"]
        == selected_result["result"]["abuf"]
    )

    assert observation_db["protocol"]["query_name"] is not None
    assert observation_db["protocol"]["query_type"] is not None
    assert observation_db["protocol"]["rcode"] is not None
    assert observation_db["protocol"]["answer_count"] >= 1