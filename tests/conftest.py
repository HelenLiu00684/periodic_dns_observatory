"""
============================================================
Project : DNS Measurement Platform
Module  : conftest.py

Description
-----------
Provides reusable pytest fixtures shared by test modules.

This module only provides test database connections.

The test database itself is created and seeded by:

    tests/database/build_test_database.py

Author
------
Helen Liu
============================================================
"""

import pytest

from periodic_dns_observatory.config.database_config import (
    TEST_DATABASE_PATH,
)

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)


@pytest.fixture
def db_connection():
    """
    Provide a SQLite connection to the platform test database.

    Responsibilities
    ----------------
    ✓ Open connection to TEST_DATABASE_PATH

    ✓ Yield connection to pytest

    ✓ Close connection after test execution

    This fixture DOES NOT
    ---------------------
    ✗ Create database schema

    ✗ Insert test data

    ✗ Delete test database

    Returns
    -------
    sqlite3.Connection
    """

    connection = get_connection(
        TEST_DATABASE_PATH,
    )

    try:
        yield connection

    finally:
        close_connection(
            connection,
        )