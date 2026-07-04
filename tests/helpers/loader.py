"""
============================================================
Project : DNS Measurement Platform

Test Helper

Load real RIPE Atlas JSON data.

All integration tests should use this loader instead of
creating fake data.
============================================================
"""

import json
from pathlib import Path


#
# Project data directory
#
DATA_DIRECTORY = Path("data")

METADATA_DIRECTORY = DATA_DIRECTORY / "metadata"

PROBE_DIRECTORY = DATA_DIRECTORY / "probes"

RAW_DIRECTORY = DATA_DIRECTORY / "raw"


# ----------------------------------------------------------
# Measurement
# ----------------------------------------------------------

def load_measurement():

    file = METADATA_DIRECTORY / "measurement_metadata.json"

    with open(file, "r") as f:

        return json.load(f)


# ----------------------------------------------------------
# Probe
# ----------------------------------------------------------

def load_probe(
    probe_id: int,
):

    file = PROBE_DIRECTORY / f"{probe_id}.json"

    with open(file, "r") as f:

        return json.load(f)


# ----------------------------------------------------------
# Results
# ----------------------------------------------------------

def load_results():

    file = RAW_DIRECTORY / "results.json"

    with open(file, "r") as f:

        return json.load(f)