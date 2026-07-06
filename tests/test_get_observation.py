"""
============================================================
Project : DNS Measurement Platform
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

        probe_path = (
            data_dir / "probes" / f"{probe_id}.json"
        )

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
    # Save
    # ======================================================

    save_all(
        db_connection,
        measurement,
        probe,
        observation,
    )

    # ======================================================
    # Read back
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
    # Measurement
    # ======================================================

    assert measurement_db is not None

    assert (
        measurement_db["measurement_id"]
        == measurement["id"]
    )

    assert (
        measurement_db["description"]
        == measurement["description"]
    )

    assert (
        measurement_db["target"]
        == measurement["target"]
    )

    assert (
        measurement_db["interval_seconds"]
        == measurement["interval"]
    )

    assert (
        measurement_db["protocol"]
        == measurement["type"]
    )

    assert (
        measurement_db["address_family"]
        == measurement["af"]
    )

    # ======================================================
    # Probe
    # ======================================================

    assert probe_db is not None

    assert (
        probe_db["probe_id"]
        == probe["id"]
    )

    assert (
        probe_db["asn_v4"]
        == probe.get("asn_v4")
    )

    assert (
        probe_db["country_code"]
        == probe.get("country_code")
    )

    assert (
        probe_db["description"]
        == probe.get("description")
    )

    # ======================================================
    # Observation
    # ======================================================

    assert observation_db is not None

    #
    # Identity
    #

    assert (
        observation_db["identity"]["observation_id"]
        == observation["identity"]["observation_id"]
    )

    assert (
        observation_db["identity"]["measurement_id"]
        == observation["identity"]["measurement_id"]
    )

    assert (
        observation_db["identity"]["probe_id"]
        == observation["identity"]["probe_id"]
    )

    #
    # Metadata
    #

    assert (
        observation_db["metadata"]["timestamp"]
        == observation["metadata"]["timestamp"]
    )

    assert (
        observation_db["metadata"]["stored_timestamp"]
        == observation["metadata"]["stored_timestamp"]
    )

    assert (
        observation_db["metadata"]["observation_type"]
        == "DNS"
    )

    #
    # Network
    #

    assert (
        observation_db["network"]["resolver_ip"]
        == observation["network"]["resolver_ip"]
    )

    assert (
        observation_db["network"]["destination_port"]
        == observation["network"]["destination_port"]
    )

    assert (
        observation_db["network"]["transport_protocol"]
        == observation["network"]["transport_protocol"]
    )

    assert (
        observation_db["network"]["response_time"]
        == observation["network"]["response_time"]
    )

    #
    # Protocol
    #

    assert (
        observation_db["protocol"]["transaction_id"]
        == observation["protocol"]["transaction_id"]
    )

    assert (
        observation_db["protocol"]["flags"]
        == observation["protocol"]["flags"]
    )

    assert (
        observation_db["protocol"]["opcode"]
        == observation["protocol"]["opcode"]
    )

    assert (
        observation_db["protocol"]["rcode"]
        == observation["protocol"]["rcode"]
    )

    assert (
        observation_db["protocol"]["query_name"]
        == observation["protocol"]["query_name"]
    )

    assert (
        observation_db["protocol"]["query_type"]
        == observation["protocol"]["query_type"]
    )

    assert (
        observation_db["protocol"]["query_class"]
        == observation["protocol"]["query_class"]
    )

    assert (
        observation_db["protocol"]["answer_count"]
        == observation["protocol"]["answer_count"]
    )

    assert (
        observation_db["protocol"]["answers"]
        == observation["protocol"]["answers"]
    )

    assert (
        observation_db["protocol"]["ttl"]
        == observation["protocol"]["ttl"]
    )

    assert (
        observation_db["protocol"]["authority_count"]
        == observation["protocol"]["authority_count"]
    )

    assert (
        observation_db["protocol"]["authority"]
        == observation["protocol"]["authority"]
    )

    assert (
        observation_db["protocol"]["additional_count"]
        == observation["protocol"]["additional_count"]
    )

    assert (
        observation_db["protocol"]["additional"]
        == observation["protocol"]["additional"]
    )

    assert (
        observation_db["protocol"]["packet_size"]
        == observation["protocol"]["packet_size"]
    )

    assert (
        observation_db["protocol"]["raw_abuf"]
        == observation["protocol"]["raw_abuf"]
    )