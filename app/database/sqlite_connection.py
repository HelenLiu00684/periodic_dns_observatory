"""
============================================================
Project : DNS Measurement Platform
Module  : database.py

Description
-----------
Provides SQLite database connection management for the
West Africa DNS Observatory.

This module is the only component responsible for creating
and managing SQLite database connections.

All database operations (Schema, Writer, Reader, FastAPI)
should obtain their database connection through this module.

Responsibilities
----------------
✓ Create SQLite connection

✓ Close SQLite connection

✓ Centralize database configuration

This module DOES NOT

✗ Create tables

✗ Insert records

✗ Query records

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


# ==========================================================
# Constants
# ==========================================================

DATABASE_NAME = "dns_measurement.db"
# DATABASE_NAME = "archive.db"

DATABASE_DIRECTORY = Path("data")




# ==========================================================
# Public Functions
# ==========================================================

def get_connection(
    database_name: str = DATABASE_NAME,
) -> sqlite3.Connection:
    """
    Create a SQLite database connection.

    Returns
    -------
    sqlite3.Connection

        SQLite connection object.
    """

    DATABASE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    database_path = DATABASE_DIRECTORY / database_name

    connection = sqlite3.connect(
        database_path
    )

    # Return query results as dictionary-like Row objects
    # instead of tuples.
    #
    # Without row_factory:
    #     row[0]
    #     row[1]
    #
    # With sqlite3.Row:
    #     row["country"]
    #     row["asn"]
    #
    # This improves readability and avoids index-related bugs
    # when table schemas change.
    connection.row_factory = sqlite3.Row

    return connection


def close_connection(
    connection: sqlite3.Connection,
) -> None:
    """
    Close an existing SQLite connection.
    """

    if connection:

        connection.close()


# ==========================================================
# Main
#
# Used only for standalone module testing.
#
# This block is executed only when this file is run directly,
# for example:
#
#     python -m app.database.database
#
# It is NOT executed when the module is imported by other
# modules such as:
#
#     sqlite_schema.py
#     sqlite_writer.py
#     sqlite_reader.py
#     FastAPI
#
# Purpose:
#     Verify that the SQLite connection can be created and
#     closed successfully.
# ==========================================================

if __name__ == "__main__":

    connection = get_connection()

    print("Database Connected")

    close_connection(connection)

    print("Database Closed")