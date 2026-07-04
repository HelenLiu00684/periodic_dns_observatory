"""
============================================================
Project : DNS Measurement Platform
Module  : sqlite_writer.py

Description
-----------
Writes normalized Observation data into the SQLite archive
database.

This module is responsible ONLY for INSERT operations.

Responsibilities
----------------
✓ Insert Measurement

✓ Insert Probe

✓ Insert Observation

✓ Prevent duplicate records

This module DOES NOT

✗ Parse DNS packets

✗ Normalize observations

✗ Perform analytics

✗ Generate telemetry

Author
------
Helen Liu
============================================================
"""

import json
from sqlite3 import Connection

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)


# ==========================================================
# Measurement
# Field Mapping
#
# RIPE Atlas JSON          SQLite Column
# --------------------------------------
# id                    -> measurement_id
# type                  -> protocol
# interval              -> interval_seconds
# af                    -> address_family
# ==========================================================

def insert_measurement(
    connection: Connection,
    measurement: dict,
) -> None:
    """
    Insert a Measurement record.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO measurement (
            measurement_id,
            description,
            target,
            interval_seconds,
            protocol,
            address_family,
            start_time,
            stop_time,
            raw_json
        )
        VALUES (
            ?,?,?,?,?,?,?,?,?
        )
        """,
        (
            measurement.get("id"),
            measurement.get("description"),
            measurement.get("target"),
            measurement.get("interval"),
            measurement.get("type"),
            measurement.get("af"),
            measurement.get("start_time"),
            measurement.get("stop_time"),
            json.dumps(measurement),
        ),
    )


# ==========================================================
# Probe
# ==========================================================

def insert_probe(
    connection: Connection,
    probe: dict,
) -> None:
    """
    Insert a Probe record.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO probe (
            probe_id,
            asn_v4,
            asn_v6,
            country_code,
            latitude,
            longitude,
            description,
            address_v4,
            address_v6,
            prefix_v4,
            prefix_v6,
            first_connected,
            status_name,
            raw_json
        )
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            probe.get("id"),
            probe.get("asn_v4"),
            probe.get("asn_v6"),
            probe.get("country_code"),
            probe.get("latitude"),
            probe.get("longitude"),
            probe.get("description"),
            probe.get("address_v4"),
            probe.get("address_v6"),
            probe.get("prefix_v4"),
            probe.get("prefix_v6"),
            probe.get("first_connected"),
            probe.get("status_name"),
            json.dumps(probe),
        ),
    )

# ==========================================================
# Observation
# ==========================================================

def insert_observation(
    connection: Connection,
    observation: dict,
) -> None:
    """
    Insert one Observation record.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO observation (
            observation_id,
            measurement_id,
            probe_id,
            timestamp,
            stored_timestamp,
            observation_type,
            identity,
            metadata,
            network,
            address_family,
            location,
            protocol,
            routing,
            path,
            telemetry,
            created_at
        )
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP
        )
        """,
        (
            observation["identity"]["observation_id"],
            observation["identity"]["measurement_id"],
            observation["identity"]["probe_id"],

            observation["metadata"]["timestamp"],
            observation["metadata"]["stored_timestamp"],
            observation["metadata"]["observation_type"],

            json.dumps(observation["identity"]),
            json.dumps(observation["metadata"]),
            json.dumps(observation["network"]),
            json.dumps(observation["address_family"]),
            json.dumps(observation["location"]),
            json.dumps(observation["protocol"]),
            json.dumps(observation["routing"]),
            json.dumps(observation["path"]),
            json.dumps(observation["telemetry"]),
        ),
    )

# ==========================================================
# Helper fetch the first one
# ==========================================================

def observation_exists(
    connection: Connection,
    observation_id: str,
) -> bool:
    """
    Check whether an Observation already exists.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT observation_id
        FROM observation
        WHERE observation_id = ?
        """,
        (observation_id,),
    )

    return cursor.fetchone() is not None


# ==========================================================
# High-Level API
# ==========================================================

# ==========================================================
# High-Level API
# ==========================================================

def save_all(
    connection: Connection,
    measurement: dict,
    probe: dict,
    observation: dict,
) -> bool:
    """
    Save a complete Observation workflow into SQLite.

    Returns
    -------
    True
        A new Observation was inserted.

    False
        Observation already exists.
    """

    insert_measurement(
        connection,
        measurement,
    )

    insert_probe(
        connection,
        probe,
    )

    observation_id = observation["identity"]["observation_id"]

    if observation_exists(
        connection,
        observation_id,
    ):

        connection.commit()

        return False

    insert_observation(
        connection,
        observation,
    )

    connection.commit()

    return True
# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("SQLite Writer Module")