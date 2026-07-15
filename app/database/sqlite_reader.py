"""
============================================================
Project : DNS Measurement Platform
Module  : sqlite_reader.py

Description
-----------
Provides archive data retrieval for the DNS Measurement Platform.

This module reads canonical platform data from the SQLite
Archive Database and returns standard Python dictionaries to
higher platform layers.

Responsibilities
----------------
✓ Fetch Measurement records
✓ Fetch Probe records
✓ Fetch Observation records
✓ Restore serialized Observation sections
✓ Return canonical Python dictionaries
✓ Support incremental telemetry retrieval
✓ Support FastAPI / dashboard latest-observation queries

This module DOES NOT
--------------------
✗ Create database connections
✗ Create database tables
✗ Insert archive records
✗ Update archive records
✗ Generate telemetry metrics
✗ Perform analytics
✗ Manage platform operations statistics

Design Principle
----------------
Database-specific objects such as sqlite3.Row and serialized
JSON strings must not escape the Database Layer.

Public Reader APIs return standard Python dictionaries so
higher platform layers remain independent of SQLite.

Primary Consumers
-----------------
This module primarily serves:

✓ Telemetry Builder
✓ Telemetry Pipeline
✓ FastAPI REST APIs
✓ React Dashboard
✓ Engineering CLI tools

Each public Reader API is designed for one or more platform
components.

Author
------
Helen Liu
============================================================
"""

import json
from sqlite3 import Connection


# ==========================================================
# Measurement
# ==========================================================

def fetch_measurement(
    connection: Connection,
    measurement_id: int,
) -> dict | None:
    """
    Fetch one canonical Measurement object from the archive.

    The returned object is fully restored and ready for use
    by higher platform layers.
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

    measurement = dict(row)

    # ------------------------------------------------------
    # Engineering Note
    #
    # measurement is already a Python dictionary because
    # sqlite3.Row has been converted using dict().
    #
    # However:
    #
    #     measurement["raw_json"]
    #
    # is still a serialized JSON string.
    #
    # The Writer Layer stored this field using json.dumps().
    #
    # Before restoration:
    #
    #     type(measurement["raw_json"]) -> str
    #
    # json.loads() restores the original Python dictionary.
    #
    # After restoration:
    #
    #     type(measurement["raw_json"]) -> dict
    #
    # Higher platform layers therefore receive structured
    # Python objects rather than serialized JSON strings.
    # ------------------------------------------------------

    if measurement["raw_json"]:
        measurement["raw_json"] = json.loads(
            measurement["raw_json"],
        )

    return measurement


# ==========================================================
# Probe
# ==========================================================

def fetch_probe(
    connection: Connection,
    probe_id: int,
) -> dict | None:
    """
    Fetch one canonical Probe object from the archive.

    The returned object is fully restored and ready for use
    by higher platform layers.
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

    probe = dict(row)

    # ------------------------------------------------------
    # Engineering Note
    #
    # probe is already a Python dictionary because sqlite3.Row
    # has been converted using dict().
    #
    # However:
    #
    #     probe["raw_json"]
    #
    # is still a serialized JSON string.
    #
    # The Writer Layer stored this field using json.dumps().
    #
    # Before restoration:
    #
    #     type(probe["raw_json"]) -> str
    #
    # json.loads() restores the original Python dictionary.
    #
    # After restoration:
    #
    #     type(probe["raw_json"]) -> dict
    #
    # Higher platform layers therefore receive structured
    # Python objects rather than serialized JSON strings.
    # ------------------------------------------------------

    if probe["raw_json"]:
        probe["raw_json"] = json.loads(
            probe["raw_json"],
        )

    return probe


# ==========================================================
# Observation
# ==========================================================

def fetch_observation(
    connection: Connection,
    observation_id: str,
) -> dict | None:
    """
    Fetch one canonical Observation record from the archive.

    This API is used when a platform component needs one
    specific Observation by observation_id.
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

    return _restore_observation(row)


# ==========================================================
# Observation Restoration
# ==========================================================

def _restore_observation(row) -> dict:
    """
    Restore one archived Observation into a canonical dictionary.

    Purpose
    -------
    SQLite stores each Observation section as a serialized JSON
    string because SQLite cannot store nested Python dictionaries
    directly.

    The Writer Layer performs this transformation before storage:

        Python dict
            ↓
        json.dumps(...)
            ↓
        SQLite TEXT

    This helper performs the reverse transformation after reading:

        SQLite TEXT
            ↓
        json.loads(...)
            ↓
        Python dict

    Before restoration:

        observation["identity"]          -> str
        observation["metadata"]          -> str
        observation["network"]           -> str
        observation["address_family"]    -> str
        observation["location"]          -> str
        observation["protocol"]          -> str
        observation["routing"]           -> str
        observation["path"]              -> str
        observation["telemetry"]         -> str

    After restoration:

        observation["identity"]          -> dict
        observation["metadata"]          -> dict
        observation["network"]           -> dict
        observation["address_family"]    -> dict
        observation["location"]          -> dict
        observation["protocol"]          -> dict
        observation["routing"]           -> dict
        observation["path"]              -> dict
        observation["telemetry"]         -> dict

    This function is the deserialization center of the Database
    Layer.

    Higher platform layers, such as the Telemetry Builder, FastAPI,
    React frontend, and Analytics Layer, always receive a fully
    restored canonical Observation and never interact with SQLite
    rows or serialized JSON strings directly.

    This helper is intentionally private.

    External platform components should retrieve Observations
    through public Reader APIs rather than calling
    _restore_observation() directly.
    """

    observation = dict(row)

    observation["identity"] = json.loads(
        observation["identity"],
    )

    observation["metadata"] = json.loads(
        observation["metadata"],
    )

    observation["network"] = json.loads(
        observation["network"],
    )

    observation["address_family"] = json.loads(
        observation["address_family"],
    )

    observation["location"] = json.loads(
        observation["location"],
    )

    observation["protocol"] = json.loads(
        observation["protocol"],
    )

    observation["routing"] = json.loads(
        observation["routing"],
    )

    observation["path"] = json.loads(
        observation["path"],
    )

    observation["telemetry"] = json.loads(
        observation["telemetry"],
    )

    # Return one fully reconstructed canonical Observation.
    return observation


# ==========================================================
# Latest Observation Retrieval
# ==========================================================

def fetch_latest_observations(
    connection: Connection,
    limit: int = 20,
) -> list[dict]:
    """
    Fetch the most recent Observation records.

    Typical Use Cases
    -----------------
    • FastAPI endpoint:
        GET /api/observations/latest

    • React dashboard:
        Display recent archive records.

    • Engineering CLI:
        Quickly inspect the latest archived observations.

    • Archive Viewer:
        Preview recent platform activity.

    Design Notes
    ------------
    The default limit is intentionally small.

    limit = 20 is designed for interactive queries, dashboards,
    API previews, and quick archive inspection.

    This is not a magic number for telemetry processing.

    This API is optimized for interactive archive browsing.

    Large-scale telemetry synchronization should use:

        fetch_incremental_telemetry_observations()

    because that API supports checkpoint-based incremental
    processing.
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

    rows = cursor.fetchall()

    # ------------------------------------------------------
    # Engineering Note
    #
    # fetchall() returns:
    #
    #     list[sqlite3.Row]
    #
    # Each sqlite3.Row represents one archived Observation.
    #
    # The following loop restores every Row into one canonical
    # Observation dictionary.
    #
    # The final observations object therefore becomes:
    #
    #     list[dict]
    #
    # rather than:
    #
    #     list[sqlite3.Row]
    # ------------------------------------------------------

    observations = []

    for row in rows:
        observations.append(
            _restore_observation(row),
        )

    return observations


# ==========================================================
# Incremental Telemetry Retrieval
# ==========================================================

def fetch_incremental_telemetry_observations(
    connection: Connection,
    last_processed_timestamp: int,
    limit: int = 1000,
) -> list[dict]:
    """
    Fetch newly archived Observations for telemetry processing.

    Purpose
    -------
    Return Observation records that have not yet been processed
    by the Telemetry Pipeline.

    Parameters
    ----------
    connection
        SQLite archive connection.

    last_processed_timestamp
        Timestamp of the last Observation successfully processed
        by the Telemetry Pipeline.

        This value is a telemetry checkpoint, not simply a generic
        database timestamp.

    limit
        Maximum number of Observation records to fetch in one
        batch.

    Typical Use Cases
    -----------------
    • Telemetry Pipeline

    • Historical Telemetry Import

    • Incremental Batch Processing

    • Checkpoint-based archive synchronization

    Typical Workflow
    ----------------

        Telemetry Pipeline

                │

                ▼

        last_processed_timestamp

                │

                ▼

        fetch_incremental_telemetry_observations()

                │

                ▼

        New canonical Observations

                │

                ▼

        Telemetry Builder

                │

                ▼

        InfluxDB

                │

                ▼

        Update last_processed_timestamp

    Design Notes
    ------------
    This API is designed for incremental processing.

    It avoids repeatedly scanning the entire archive by fetching
    only records with:

        timestamp > last_processed_timestamp

    Returned objects are still raw canonical Observations.

    Telemetry metric generation happens later in the Telemetry
    Builder Layer.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM observation
        WHERE timestamp > ?
        ORDER BY timestamp
        LIMIT ?
        """,
        (
            last_processed_timestamp,
            limit,
        ),
    )

    rows = cursor.fetchall()

    # ------------------------------------------------------
    # Engineering Note
    #
    # fetchall() returns:
    #
    #     list[sqlite3.Row]
    #
    # Each sqlite3.Row represents one archived Observation.
    #
    # The following loop restores every Row into one canonical
    # Observation dictionary.
    #
    # The final observations object therefore becomes:
    #
    #     list[dict]
    #
    # rather than:
    #
    #     list[sqlite3.Row]
    # ------------------------------------------------------

    observations = []

    for row in rows:

        # --------------------------------------------------
        # Engineering Note
        #
        # Each sqlite3.Row represents one archived Observation.
        #
        # _restore_observation() reconstructs that archived
        # record into one canonical Observation dictionary.
        #
        # observations therefore becomes:
        #
        #     list[dict]
        #
        # rather than:
        #
        #     list[sqlite3.Row]
        #
        # Every element inside observations is a fully restored
        # canonical Observation.
        #
        # Downstream components such as the Telemetry Builder
        # process canonical Observation dictionaries directly
        # without interacting with SQLite-specific rows or
        # serialized JSON strings.
        # --------------------------------------------------

        observations.append(
            _restore_observation(row),
        )

    return observations


# ==========================================================
# Standalone Verification
# ==========================================================

if __name__ == "__main__":

    print("SQLite Reader Module")