"""
============================================================
Project : DNS Measurement Platform
Module  : sqlite_schema.py

Description
-----------
Provides schema management for the SQLite Archive Database.

This module defines the complete archive schema used by the
DNS Measurement Platform.

SQLite serves as the platform's Archive Database. It stores
complete normalized Observation records but is not responsible
for telemetry generation, visualization, or analytics.

Responsibilities
----------------
✓ Create archive database tables

✓ Drop archive database tables

✓ Initialize the archive schema

✓ Reset the database during development and testing

This module DOES NOT
--------------------
✗ Create database connections

✗ Insert archive records

✗ Read archive records

✗ Generate telemetry metrics

✗ Perform analytics

Design Principle
----------------
Schema management is intentionally separated from connection
management, archive persistence, and archive retrieval.

Author
------
Helen Liu
============================================================
"""

from sqlite3 import Connection

from app.database.sqlite_connection import (
    close_connection,
    get_connection,
)


# ==========================================================
# Public APIs
# ==========================================================

def create_tables(connection: Connection) -> None:
    """
    Create the complete SQLite archive schema.

    This function creates every table required by the DNS
    Measurement Platform.

    Table creation is delegated to dedicated helper functions
    so each table remains independently maintainable.

    This function is typically executed during platform
    initialization.
    """

    create_measurement_table(connection)
    create_probe_table(connection)
    create_observation_table(connection)

    connection.commit()


def create_measurement_table(connection: Connection) -> None:
    """
    Create the Measurement table.

    Purpose
    -------
    Store RIPE Atlas measurement metadata.

    One measurement may generate observations from many
    probes over time.

    Measurement records are therefore stored independently
    and referenced by Observation through measurement_id.

    One measurement_id should appear only once.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS measurement (
            measurement_id INTEGER PRIMARY KEY,
            description TEXT,
            target TEXT,
            interval_seconds INTEGER,
            protocol TEXT,
            address_family INTEGER,
            start_time INTEGER,
            stop_time INTEGER,
            raw_json TEXT
        );
        """
    )


def create_probe_table(connection: Connection) -> None:
    """
    Create the Probe table.

    Purpose
    -------
    Store RIPE Atlas probe metadata.

    One probe may participate in many observations during
    its lifetime.

    Probe metadata is stored separately to avoid duplication
    across Observation records.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS probe (
            probe_id INTEGER PRIMARY KEY,
            asn_v4 INTEGER,
            asn_v6 INTEGER,
            country_code TEXT,
            latitude REAL,
            longitude REAL,
            description TEXT,
            address_v4 TEXT,
            address_v6 TEXT,
            prefix_v4 TEXT,
            prefix_v6 TEXT,
            first_connected INTEGER,
            status_name TEXT,
            raw_json TEXT
        );
        """
    )


def create_observation_table(connection: Connection) -> None:
    """
    Create the Observation table.

    Purpose
    -------
    Store complete canonical Observation records.

    SQLite acts as the platform Archive Database rather than
    a telemetry database.

    JSON sections are stored as TEXT so the complete
    Observation structure can be preserved without flattening
    every field into relational columns.

    The Database Layer stores Observation records only.

    Interpretation of JSON contents belongs to higher layers,
    such as the Telemetry Pipeline, REST API, or Analytics.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS observation (
            observation_id TEXT PRIMARY KEY,

            measurement_id INTEGER,
            probe_id INTEGER,

            timestamp INTEGER,
            stored_timestamp INTEGER,
            observation_type TEXT,

            identity TEXT,
            metadata TEXT,
            network TEXT,
            address_family TEXT,
            location TEXT,
            protocol TEXT,
            routing TEXT,
            path TEXT,
            telemetry TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (measurement_id)
                REFERENCES measurement(measurement_id),

            FOREIGN KEY (probe_id)
                REFERENCES probe(probe_id)
        );
        """
    )


def drop_tables(connection: Connection) -> None:
    """
    Drop all archive tables.

    This function is intended only for local development and
    automated testing.

    Production archive databases should never be reset by
    application logic.
    """

    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS observation;")
    cursor.execute("DROP TABLE IF EXISTS probe;")
    cursor.execute("DROP TABLE IF EXISTS measurement;")

    connection.commit()


def reset_database() -> None:
    """
    Recreate the complete archive database.

    This helper is primarily intended for local development,
    automated testing, and engineering tools.

    Production systems should initialize databases without
    deleting existing archive data.
    """

    connection = get_connection()

    try:
        drop_tables(connection)
        create_tables(connection)

    finally:
        close_connection(connection)


def initialize_database() -> None:
    """
    Initialize the SQLite archive database.

    Safe to execute multiple times.

    Existing tables remain unchanged because every CREATE
    TABLE statement uses IF NOT EXISTS.
    """

    connection = get_connection()

    try:
        create_tables(connection)

    finally:
        close_connection(connection)

# ==========================================================
# Public Schema Builder
# ==========================================================

def create_database_schema(
    connection: Connection,
) -> None:
    """
    Create the complete SQLite database schema.

    This function is the primary entry point for database
    initialization.

    It creates every table and index required by the
    DNS Measurement Platform.

    Typical Use Cases
    -----------------
    • Production database initialization

    • Test database creation

    • Database reset scripts

    • Platform deployment

    Engineering Notes
    -----------------
    This function is an orchestration API.

    It does not execute SQL directly.

    Instead, it delegates schema creation to the
    individual table builders defined in this module.

    Returns
    -------
    None
    """

    create_measurement_table(
        connection,
    )

    create_probe_table(
        connection,
    )

    create_observation_table(
        connection,
    )

    connection.commit()


# ==========================================================
# Standalone Verification
# ==========================================================

if __name__ == "__main__":

    initialize_database()

    print("SQLite archive schema initialized.")