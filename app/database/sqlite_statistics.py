"""
============================================================
Project : DNS Measurement Platform
Module  : sqlite_statistics.py

Description
-----------
Provides lightweight archive statistics for platform
operations.

Unlike sqlite_reader.py, this module does not retrieve
canonical Measurement, Probe, or Observation objects.

Instead, it provides operational information about the
SQLite archive itself.

Typical Use Cases
-----------------
✓ database_status.sh

✓ archive_summary.sh

✓ platform_status.sh

✓ health_check.sh

✓ Future FastAPI health endpoint

✓ Engineering CLI utilities

This module DOES NOT
--------------------
✗ Return canonical business objects

✗ Restore Observation dictionaries

✗ Generate telemetry metrics

✗ Perform analytics

Design Principle
----------------
Platform operation scripts often need lightweight archive
statistics rather than complete business objects.

Separating archive statistics from sqlite_reader.py keeps
business data retrieval independent from platform
monitoring.

Author
------
Helen Liu
============================================================
"""

from sqlite3 import Connection


# ==========================================================
# Measurement Statistics
# ==========================================================

def fetch_measurement_count(
    connection: Connection,
) -> int:
    """
    Return the total number of archived Measurement records.

    Typical Use Cases
    -----------------
    • database_status.sh

    • archive_summary.sh

    • Platform health monitoring

    Engineering Note
    ----------------
    fetchone() always returns ONE database row.

    Even when SQL returns only a single value such as:

        SELECT COUNT(*)

    SQLite represents the result as:

        (15,)

    [0] accesses the FIRST element of the tuple,
    which is also the only column returned by the SQL query.

    Returns
    -------
    int

    Total number of archived Measurement records.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM measurement
        """
    )

    return cursor.fetchone()[0]


# ==========================================================
# Probe Statistics
# ==========================================================

def fetch_probe_count(
    connection: Connection,
) -> int:
    """
    Return the total number of archived Probe records.

    Returns
    -------
    int

    Total number of archived Probe records.

    See fetch_measurement_count() for an explanation of
    fetchone()[0].
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM probe
        """
    )

    return cursor.fetchone()[0]


# ==========================================================
# Observation Statistics
# ==========================================================

def fetch_observation_count(
    connection: Connection,
) -> int:
    """
    Return the total number of archived Probe records.

    Returns
    -------
    int

    Total number of archived Probe records.

    See fetch_measurement_count() for an explanation of
    fetchone()[0].
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM observation
        """
    )

    return cursor.fetchone()[0]


# ==========================================================
# Archive Time Range
# ==========================================================

def fetch_archive_time_range(
    connection: Connection,
) -> tuple[int | None, int | None]:
    """
    Return the oldest and newest Observation timestamps.

    Returns
    -------
    tuple[int | None, int | None]

        (
            oldest_timestamp,
            latest_timestamp,
        )

    Returns (None, None) if the Observation table is empty.

    Engineering Note
    ----------------
    This SQL query returns TWO columns:

        MIN(timestamp)

        MAX(timestamp)

    fetchone() therefore returns one tuple:

        (
            oldest_timestamp,
            latest_timestamp,
        )

    The caller normally unpacks the tuple:

        oldest_timestamp, latest_timestamp = \
            fetch_archive_time_range(...)
    """

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
# Latest IDs
# ==========================================================

def fetch_latest_measurement_id(
    connection: Connection,
) -> int | None:
    """
    Return the largest Measurement ID currently stored
    in the archive.

    Returns
    -------
    int | None

    Largest Measurement ID currently stored in the archive.

    Returns None if the Measurement table is empty.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT MAX(measurement_id)
        FROM measurement
        """
    )

    return cursor.fetchone()[0]


def fetch_latest_probe_id(
    connection: Connection,
) -> int | None:
    """
    Return the largest Probe ID currently stored
    in the archive.

    Returns
    -------
    int | None

    Largest Probe ID currently stored in the archive.

    Returns None if the Probe table is empty.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT MAX(probe_id)
        FROM probe
        """
    )

    return cursor.fetchone()[0]


# ==========================================================
# Database Summary
# ==========================================================

def fetch_database_summary(
    connection: Connection,
) -> dict:
    """
    Return a lightweight summary of the archive database.

    Purpose
    -------
    This API is designed for platform operations rather than
    telemetry processing.

    Typical Use Cases
    -----------------
    • database_status.sh

    • archive_summary.sh

    • platform_status.sh

    • health_check.sh

    • Future FastAPI health endpoint

    Returns
    -------
    dict

    A lightweight archive summary.

    Example

    {
        "measurement_count": 10,
        "probe_count": 683,
        "observation_count": 125384,
        "oldest_timestamp": 1751511000,
        "latest_timestamp": 1751519999,
        "latest_measurement_id": 1001,
        "latest_probe_id": 683,
    }
    """

    oldest_timestamp, latest_timestamp = (
        fetch_archive_time_range(
            connection,
        )
    )

    return {

        "measurement_count":
            fetch_measurement_count(connection),

        "probe_count":
            fetch_probe_count(connection),

        "observation_count":
            fetch_observation_count(connection),

        "oldest_timestamp":
            oldest_timestamp,

        "latest_timestamp":
            latest_timestamp,

        "latest_measurement_id":
            fetch_latest_measurement_id(connection),

        "latest_probe_id":
            fetch_latest_probe_id(connection),
    }


# ==========================================================
# Standalone Verification
# ==========================================================

if __name__ == "__main__":

    print("SQLite Statistics Module")