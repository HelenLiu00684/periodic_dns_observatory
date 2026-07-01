"""
============================================================
Project : West Africa DNS Observatory
Module  : sqlite_reader.py

Description
-----------
Reads archive data from the SQLite database.

This module is responsible ONLY for SELECT operations.

Responsibilities
----------------
✓ Read Measurement

✓ Read Probe

✓ Read Observation

✓ List Observations

This module DOES NOT

✗ Parse DNS packets

✗ Normalize observations

✗ Insert records

✗ Update records

✗ Perform analytics

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
# ==========================================================

def get_measurement(
    connection: Connection,
    measurement_id: int,
) -> dict | None:
    """
    Read one Measurement.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM measurement
        WHERE measurement_id = ?
        """,
        (measurement_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return dict(row)


# ==========================================================
# Probe
# ==========================================================

def get_probe(
    connection: Connection,
    probe_id: int,
) -> dict | None:
    """
    Read one Probe.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM probe
        WHERE probe_id = ?
        """,
        (probe_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return dict(row)


# ==========================================================
# Observation
# ==========================================================

def get_observation(
    connection: Connection,
    observation_id: str,
) -> dict | None:
    """
    Read one Observation.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM observation
        WHERE observation_id = ?
        """,
        (observation_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    observation = dict(row)

    #
    # Restore JSON fields
    #
    observation["identity"] = json.loads(observation["identity"])
    observation["metadata"] = json.loads(observation["metadata"])
    observation["network"] = json.loads(observation["network"])
    observation["address_family"] = json.loads(observation["address_family"])
    observation["location"] = json.loads(observation["location"])
    observation["protocol"] = json.loads(observation["protocol"])
    observation["routing"] = json.loads(observation["routing"])
    observation["path"] = json.loads(observation["path"])
    observation["telemetry"] = json.loads(observation["telemetry"])

    return observation


# ==========================================================
# List
# ==========================================================

def list_observations(
    connection: Connection,
) -> list[dict]:
    """
    Read all Observation records.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM observation
        ORDER BY timestamp
        """
    )

    rows = cursor.fetchall()

    observations = []

    for row in rows:

        observation = dict(row)

        observation["identity"] = json.loads(observation["identity"])
        observation["metadata"] = json.loads(observation["metadata"])
        observation["network"] = json.loads(observation["network"])
        observation["address_family"] = json.loads(observation["address_family"])
        observation["location"] = json.loads(observation["location"])
        observation["protocol"] = json.loads(observation["protocol"])
        observation["routing"] = json.loads(observation["routing"])
        observation["path"] = json.loads(observation["path"])
        observation["telemetry"] = json.loads(observation["telemetry"])

        observations.append(observation)

    return observations


# ==========================================================
# High-Level API
# ==========================================================

def read_archive(
    observation_id: str,
) -> dict | None:
    """
    Read one Observation from the archive database.
    """

    connection = get_connection()

    try:

        return get_observation(
            connection,
            observation_id,
        )

    finally:

        close_connection(connection)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("SQLite Reader Module")