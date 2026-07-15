"""
============================================================
Project : DNS Measurement Platform
Module  : build_test_database.py

Description
-----------
Build the platform test database.

This script rebuilds the SQLite test archive from the
platform test data.

The generated database is used by:

• Pytest

• Shell test scripts

• Collector integration tests

• Telemetry tests

• FastAPI tests

Unlike the production database, the test database is
recreated from scratch before each database test.

Workflow
--------
Delete existing test database

↓

Create SQLite database

↓

Create database schema

↓

Load measurement metadata

↓

Load probe information

↓

Load raw observations

↓

Normalize observations

↓

Insert canonical objects into SQLite

↓

Generate test_archive.db

Engineering Notes
-----------------
This script DOES NOT execute SQL directly.

Instead, it reuses the Database Layer:

• sqlite_connection.py

• sqlite_schema.py

• sqlite_writer.py

This guarantees that production and test databases are
built using exactly the same APIs.

Author
------
Helen Liu
"""