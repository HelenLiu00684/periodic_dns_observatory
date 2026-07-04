"""
Pytest Fixtures

Shared fixtures used by all database tests.
"""
# ==========================================================
# Pytest Fixture
#
# A fixture is a reusable resource provider used by pytest.
#
# Instead of repeatedly creating and cleaning up the same
# resource inside every test function, pytest automatically
# executes the fixture whenever a test requests it.
#
# Example
#
#     def test_insert_measurement(db_connection):
#
# The parameter "db_connection" tells pytest to execute the
# fixture below and inject the prepared database connection
# into the test.
#
# ----------------------------------------------------------
# yield
#
# The yield statement separates the fixture into two phases.
#
# Before yield
#
#     Setup
#
#         • Create SQLite database connection
#         • Initialize database schema
#
# yield
#
#     Pass the prepared database connection to the test.
#
# After yield
#
#     Teardown
#
#         • Close database connection
#         • Remove temporary test database
#
# Using fixtures guarantees that every test starts with a
# clean, isolated database environment while avoiding
# duplicated setup code across multiple test modules.
# ==========================================================

"""
============================================================
Project : DNS Measurement Platform
Module  : conftest.py

Description
-----------
Provides reusable pytest fixtures shared by all test modules.

Fixtures are responsible for preparing and cleaning up
resources required during testing.

Responsibilities
----------------
✓ Create test database connection

✓ Initialize database schema

✓ Provide reusable resources to tests

✓ Clean up test environment

This module DOES NOT

✗ Test application logic

✗ Insert database records

✗ Query database records

✗ Validate observations

Author
------
Helen Liu
============================================================
"""
import os

import pytest

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_schema import (
    create_tables,
)


TEST_DATABASE = "dns_measurement.db"


@pytest.fixture
def db_connection():

    #
    # Create connection
    #
    connection = get_connection(TEST_DATABASE)

    #
    # Ensure schema exists
    #
    create_tables(connection)

    #
    # Give connection to the test
    #
    yield connection

    #
    # Cleanup
    #
    close_connection(connection)

    #
    # Remove test database
    #
    database_path = os.path.join(
        "data",
        TEST_DATABASE,
    )

    if os.path.exists(database_path):
        os.remove(database_path)