"""
============================================================
Project : DNS Measurement Platform
Module  : sqlite_connection.py

Description
-----------
Provides SQLite connection management for the DNS Measurement
Platform.

This module is the single entry point for creating and closing
SQLite database connections. Every database component, including
schema management, archive writer, archive reader, telemetry
pipeline, CLI tools, and automated tests, should obtain database
connections through this module.

Responsibilities
----------------
✓ Create SQLite database connections

✓ Configure connection behavior

✓ Close database connections

✓ Centralize the default database location

This module DOES NOT
--------------------
✗ Create database tables

✗ Insert archive records

✗ Read archive records

✗ Reset the database

✗ Perform telemetry or analytics processing

Design Principle
----------------
Connection management is intentionally separated from schema,
writer, and reader logic.

By centralizing connection creation in a single module, the
entire platform shares identical database configuration and
connection behavior.

Author
------
Helen Liu
============================================================
"""

# ==========================================================
# Imports
# ==========================================================

import sqlite3
from pathlib import Path

from periodic_dns_observatory.config.database_config import (
    PRODUCTION_DATABASE_PATH,
)

# ==========================================================
# Public APIs
# ==========================================================

def get_connection(
    sqlite_database_path: str | Path = PRODUCTION_DATABASE_PATH
) -> sqlite3.Connection:
    """
    Create a SQLite database connection.

    Parameters
    ----------
    sqlite_database_path : str | Path, optional

        SQLite database file.

        By default, the production archive database is used.

        Unit tests should provide their own temporary database
        to ensure complete isolation from production data.

    Returns
    -------
    sqlite3.Connection

        Configured SQLite connection object.
    """

    sqlite_database_path = Path(sqlite_database_path)

    sqlite_database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        sqlite_database_path,
    )

    # ======================================================
    # Engineering Note
    #
    # SQLite returns query results according to the
    # connection's "row_factory" attribute.
    #
    # ------------------------------------------------------
    # Default SQLite Behavior
    #
    # connection.row_factory = None
    #
    # Each row returned by fetchone() or fetchall() is a
    # standard Python tuple.
    #
    # Example
    #
    #     row = cursor.fetchone()
    #
    #     record = {
    #         "measurement_id": row[0],
    #         "description": row[1],
    #         "target": row[2],
    #     }
    #
    # This requires manual column indexing and tightly
    # couples the Reader Layer to the table schema.
    #
    # ------------------------------------------------------
    # Project Behavior
    #
    # This project configures:
    #
    #     connection.row_factory = sqlite3.Row
    #
    # Each query result is returned as a sqlite3.Row object
    # instead of a tuple.
    #
    # sqlite3.Row implements Python's mapping interface,
    # allowing rows to be converted directly into standard
    # Python dictionaries.
    #
    # Example
    #
    #     row = cursor.fetchone()
    #
    #     record = dict(row)
    #
    # The Reader Layer therefore returns standard Python
    # dictionaries instead of SQLite-specific objects.
    #
    # Database-specific sqlite3.Row objects never leave the
    # Database Layer, keeping higher platform layers
    # independent of SQLite.
    # ======================================================

    connection.row_factory = sqlite3.Row

    return connection


def close_connection(
    connection: sqlite3.Connection | None,
) -> None:
    """
    Close an existing SQLite connection.

    Parameters
    ----------
    connection : sqlite3.Connection | None

        SQLite connection to close.

        Passing None is allowed so cleanup code can safely
        execute even if connection creation failed.
    """

    if connection is not None:
        connection.close()


# ==========================================================
# Standalone Verification
# ==========================================================

if __name__ == "__main__":

    connection = get_connection()

    print("Database connected.")

    close_connection(connection)

    print("Database closed.")