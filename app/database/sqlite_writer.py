"""
============================================================
Project : DNS Measurement Platform
Module  : sqlite_writer.py

Description
-----------
Provides archive persistence for the DNS Measurement Platform.

This module stores canonical platform data into the SQLite
Archive Database.

The Writer Layer is responsible ONLY for persisting data.

It assumes all incoming objects have already been collected,
validated, and normalized by higher platform layers.

Responsibilities
----------------
✓ Insert Measurement records

✓ Insert Probe records

✓ Insert Observation records

✓ Prevent duplicate Observation records

✓ Commit archive transactions

This module DOES NOT
--------------------
✗ Create database connections

✗ Create database tables

✗ Parse RIPE Atlas responses

✗ Normalize Observation objects

✗ Generate telemetry metrics

✗ Perform analytics

Design Principle
----------------
Persistence is intentionally separated from collection,
normalization, telemetry generation, and visualization.

The Writer Layer stores canonical platform objects exactly as
they are received.

Author
------
Helen Liu
============================================================
"""

# ==========================================================
# Imports
# ==========================================================

import json
from sqlite3 import Connection

from app.database.sqlite_connection import (
    close_connection,
    get_connection,
)


# ==========================================================
# Measurement
#
# Purpose
# ----------------------------------------------------------
# Store RIPE Atlas Measurement metadata.
#
# One Measurement may generate Observation records from many
# different probes over time.
#
# Measurement therefore has an independent lifecycle and is
# stored separately from Observation records.
#
#
# RIPE Atlas JSON            SQLite Archive
# ----------------------------------------------------------
# id                     -> measurement_id
#
# type                   -> protocol
#
# interval               -> interval_seconds
#
# af                     -> address_family
#
# The complete original Measurement object is preserved in
# raw_json.
# ==========================================================

def insert_measurement(
    connection: Connection,
    measurement: dict,
) -> None:
    """
    Insert one Measurement record.

    Parameters
    ----------
    connection
        SQLite archive connection.

    measurement
        Canonical Measurement dictionary.

    Notes
    -----
    Measurement originates from an external system.

    Missing fields are therefore accepted as None using
    dict.get() instead of direct dictionary indexing.

    This prevents KeyError when optional fields are absent.
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

            # ==================================================
            # Engineering Note
            #
            # SQLite stores only primitive values such as
            # INTEGER, REAL, TEXT, BLOB, and NULL.
            #
            # Python dictionaries cannot be written directly
            # into SQLite.
            #
            # The Writer Layer therefore serializes the
            # Measurement dictionary into a JSON string before
            # persistence.
            #
            # Data Transformation
            # -------------------
            #
            # Python Dictionary
            #
            #     measurement
            #
            #            │
            #            ▼
            #
            # json.dumps(measurement):  dumps = Serialize to JSON String
            #
            #            │
            #            ▼
            #
            # JSON String (TEXT)
            #
            #            │
            #            ▼
            #
            # SQLite Archive
            #
            # During archive retrieval the Reader Layer performs
            # the reverse transformation:
            #
            #     json.loads(raw_json):  loads = Deserialize JSON String → Python Object
            #
            #            │
            #            ▼
            #
            # Python Dictionary
            #
            # Higher platform layers therefore always work with
            # standard Python dictionaries rather than JSON
            # strings.
            #
            # Serialization is considered part of persistence,
            # not business logic.
            # ==================================================

            json.dumps(measurement),
        ),
    )


# ==========================================================
# Probe
#
# Purpose
# ----------------------------------------------------------
# Store RIPE Atlas Probe metadata.
#
# One Probe may participate in many Observation records.
#
# Probe information is therefore normalized into its own
# archive table to avoid duplication.
#
# The complete original Probe object is preserved in raw_json.
# ==========================================================

def insert_probe(
    connection: Connection,
    probe: dict,
) -> None:
    """
    Insert one Probe record.

    Parameters
    ----------
    connection
        SQLite archive connection.

    probe
        Canonical Probe dictionary.

    Notes
    -----
    Probe information originates from external systems.

    Optional fields are accepted using dict.get().

    Missing values are stored as NULL inside SQLite.
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

            # Engineering Note
            #
            # Preserve the complete Probe object exactly as it
            # was received from the Collector Layer.
            #
            # Individual database columns support efficient
            # filtering and indexing, while raw_json preserves
            # the complete source object for debugging, future
            # schema evolution, and archive replay.
            json.dumps(probe),
        ),
    )
# ==========================================================
# Observation
#
# Purpose
# ----------------------------------------------------------
# Store one complete canonical Observation record.
#
# Observation is the core archive entity of the DNS
# Measurement Platform.
#
# Unlike Measurement and Probe metadata, every Observation
# represents one point-in-time network measurement.
#
# Observation objects are assumed to be fully normalized
# before entering the Writer Layer.
#
# Therefore, required fields are accessed directly using
# dictionary indexing instead of dict.get().
#
# Missing required fields should raise KeyError because they
# indicate an invalid canonical Observation.
# ==========================================================

def insert_observation(
    connection: Connection,
    observation: dict,
) -> None:
    """
    Insert one Observation record.

    Parameters
    ----------
    connection
        SQLite archive connection.

    observation
        Canonical Observation dictionary.

    Notes
    -----
    Observation is already normalized.

    Required fields are accessed directly.

    Nested Observation sections are serialized into JSON
    before being stored inside SQLite.
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

            # ==================================================
            # Engineering Note
            #
            # Observation contains multiple nested dictionaries.
            #
            # SQLite cannot store nested Python objects directly.
            #
            # Each logical Observation section is therefore
            # serialized independently.
            #
            # This preserves the original platform structure
            # while allowing future Reader implementations to
            # deserialize only the sections they require.
            #
            # Reader
            #
            #     json.loads(identity)
            #
            #     json.loads(network)
            #
            #     json.loads(routing)
            #
            # rather than reconstructing one large JSON object.
            #
            # This design keeps archive persistence independent
            # from higher platform layers.
            # ==================================================

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
# Archive Validation
# ==========================================================

def observation_exists(
    connection: Connection,
    observation_id: str,
) -> bool:
    """
    Determine whether an Observation already exists.

    Parameters
    ----------
    connection
        SQLite archive connection.

    observation_id
        Observation identifier.

    Returns
    -------
    bool

        True
            Observation already exists.

        False
            Observation does not exist.

    Notes
    -----
    Observation is the only archive entity checked for
    duplication because every Observation represents one
    immutable measurement event.
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
# Archive Workflow
# ==========================================================

def save_all(
    connection: Connection,
    measurement: dict,
    probe: dict,
    observation: dict,
) -> bool:
    """
    Persist one complete Observation workflow.

    Archive Workflow
    ----------------

        Measurement

              │

              ▼

           Probe

              │

              ▼

        Observation

              │

              ▼

          Commit

    Measurement and Probe metadata are updated whenever they
    are received.

    Observation records are inserted only if they do not
    already exist.

    Returns
    -------
    True

        A new Observation was archived.

    False

        Observation already existed.
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
# Standalone Verification
# ==========================================================

if __name__ == "__main__":

    print("SQLite Writer Module")    