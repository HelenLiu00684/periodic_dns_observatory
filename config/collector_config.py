"""
============================================================
Project : DNS Measurement Platform
Module  : config.py

Description
-----------
Centralized configuration for the Collector Layer.

This module defines:

• Measurement configuration

• RIPE Atlas API endpoint

• Collector output directories

The Collector downloads raw data from RIPE Atlas and
stores JSON files locally for later processing.

This module does NOT perform any network requests or file
operations beyond creating the required directory
structure.

Design Principle
----------------
All Collector modules should import configuration values
from this file instead of hardcoding paths or API
endpoints.

This keeps the Collector Layer consistent and easy to
maintain.

Author
------
Helen Liu
============================================================
"""

from pathlib import Path


# ==========================================================
# RIPE Atlas Measurement
# ==========================================================

# Target Measurement ID collected by the platform.
MEASUREMENT_ID = 186325158


# ==========================================================
# RIPE Atlas REST API
# ==========================================================

# Base URL for all RIPE Atlas API requests.
BASE_URL = "https://atlas.ripe.net/api/v2"


# ==========================================================
# Collector Output Directories
# ==========================================================

# Root directory used by the Collector Layer.
DATA_DIR = Path("data")

# ==========================================================
# Collector Directory
# ==========================================================

# Collector database directory.
Collector_DIRECTORY = DATA_DIR / "collector"


# Raw DNS measurement results.
RAW_DIR = Collector_DIRECTORY / "raw"

# Measurement metadata.
METADATA_DIR = Collector_DIRECTORY / "metadata"

# Individual RIPE Atlas probe metadata.
PROBE_DIR = Collector_DIRECTORY / "probes"


# ==========================================================
# Directory Initialization
# ==========================================================

# Ensure the required directory structure exists before
# downloading or saving any JSON files.
RAW_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

METADATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

PROBE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)