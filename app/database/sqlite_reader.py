"""
============================================================
Project : DNS Measurement Platform
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

import os


def get_measurement_count(connection: Connection) -> int:
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM measurement
        """
    )

    return cursor.fetchone()[0]


def get_probe_count(connection: Connection) -> int:
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM probe
        """
    )

    return cursor.fetchone()[0]


def get_observation_count(connection: Connection) -> int:
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM observation
        """
    )

    return cursor.fetchone()[0]


def get_timestamp_range(connection: Connection):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            MIN(timestamp),
            MAX(timestamp)
        FROM observation
        """
    )

    return cursor.fetchone()
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

def get_latest_measurement_id(connection: Connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT MAX(measurement_id)
        FROM measurement
        """
    )

    return cursor.fetchone()[0]


def get_latest_probe_id(connection: Connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT MAX(probe_id)
        FROM probe
        """
    )

    return cursor.fetchone()[0]


def get_database_summary(connection: Connection) -> dict:
    """
    Return overall SQLite archive statistics.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM measurement
        """
    )
    measurement_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM probe
        """
    )
    probe_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM observation
        """
    )
    observation_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT
            MIN(timestamp),
            MAX(timestamp)
        FROM observation
        """
    )

    oldest_timestamp, latest_timestamp = cursor.fetchone()

    cursor.execute(
        """
        SELECT MAX(measurement_id)
        FROM measurement
        """
    )

    latest_measurement = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT MAX(probe_id)
        FROM probe
        """
    )

    latest_probe = cursor.fetchone()[0]

    return {
        "measurement_count": measurement_count,
        "probe_count": probe_count,
        "observation_count": observation_count,
        "oldest_timestamp": oldest_timestamp,
        "latest_timestamp": latest_timestamp,
        "latest_measurement": latest_measurement,
        "latest_probe": latest_probe,
    }
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



def get_all_measurements(connection: Connection) -> list:
    """
    Return all Measurement records.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM measurement
        """
    )

    return cursor.fetchall()


def get_all_probes(connection: Connection) -> list:
    """
    Return all Probe records.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM probe
        """
    )

    return cursor.fetchall()


def get_all_observations(
    connection: Connection,
    limit: int = 20,
) -> list:
    """
    Return latest Observation records.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM observation
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )

    return cursor.fetchall()
# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("SQLite Reader Module")