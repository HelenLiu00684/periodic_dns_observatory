"""
============================================================
Project : DNS Measurement Platform
Module  : database_config.py

Description
-----------
Centralized database configuration for the DNS Measurement
Platform.

This module defines the locations of both the production
archive database and the dedicated test database.

Using a shared configuration ensures that all platform
components reference the same database paths.

Used By
-------
• SQLite Database Layer

• Collector Archive

• Pytest

• Database Utility Scripts

• FastAPI

Design Principle
----------------
All database paths are defined in one place.

Application modules should import database locations from
this module instead of hardcoding filesystem paths.

Author
------
Helen Liu
============================================================
"""

from pathlib import Path

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent
)



# ==========================================================
# Root Data Directory
# ==========================================================

# Root directory used to store all platform data.
DATA_DIRECTORY = Path("data")


# ==========================================================
# Archive Directory
# ==========================================================

# SQLite archive database directory.
ARCHIVE_DIRECTORY = DATA_DIRECTORY / "archive"


# ==========================================================
# Production Database
# ==========================================================

PRODUCTION_DATABASE_NAME = "dns_measurement.db"

PRODUCTION_DATABASE_PATH = (
    ARCHIVE_DIRECTORY
    / PRODUCTION_DATABASE_NAME
)


# ==========================================================
# Test Database
# ==========================================================

# Dedicated database used by automated testing.
TEST_DATABASE_DIRECTORY = Path(
    "tests/database"
)

TEST_DATABASE_NAME = "test_archive.db"

TEST_DATABASE_PATH = (
    TEST_DATABASE_DIRECTORY
    / TEST_DATABASE_NAME
)