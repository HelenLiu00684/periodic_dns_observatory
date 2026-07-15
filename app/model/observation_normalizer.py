"""
============================================================
Project : DNS Measurement Platform
Module  : observation_normalizer.py

Description
-----------
Coordinates all Normalizer modules to build one Canonical
Observation.

This module contains no business logic.

Each Observation section is normalized by an independent
Normalizer module.

Normalization Flow
------------------

Measurement JSON
        │
Probe JSON
        │
Result JSON
        ▼
Observation Normalizer
        │
        ├── Identity
        ├── Metadata
        ├── Measurement
        ├── Probe
        ├── Network
        ├── Location
        ├── Protocol
        ├── Routing
        ├── Path
        ├── Status
        └── Telemetry
        ▼
Canonical Observation

Design Principle
----------------
This module is an Orchestrator.

It does not:

• Parse JSON

• Normalize fields

• Decode DNS packets

• Generate telemetry

• Write SQLite

• Validate observations

Its only responsibility is coordinating the individual
Normalizer modules.

Author
------
Helen Liu
============================================================
"""

from typing import Any

from app.model.observation import create_empty_observation

from app.normalizer.identity_normalizer import normalize_identity
from app.normalizer.metadata_normalizer import normalize_metadata
from app.normalizer.measurement_normalizer import normalize_measurement
from app.normalizer.probe_normalizer import normalize_probe
from app.normalizer.network_normalizer import normalize_network
from app.normalizer.location_normalizer import normalize_location
from app.normalizer.protocol_normalizer import normalize_protocol
from app.normalizer.routing_normalizer import normalize_routing
# from app.normalizer.path_normalizer import normalize_path
# from app.normalizer.status_normalizer import normalize_status
# from app.normalizer.telemetry_normalizer import normalize_telemetry


# ==========================================================
# Public API
# ==========================================================

def normalize_dns_observation(
    measurement: dict[str, Any],
    probe: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize one RIPE Atlas DNS measurement into one
    Canonical Observation.
    """

    observation = create_empty_observation()

    observation["identity"] = normalize_identity(
        measurement,
        probe,
        result,
    )

    observation["metadata"] = normalize_metadata(
        result,
    )

    observation["measurement"] = normalize_measurement(
        measurement,
    )

    observation["probe"] = normalize_probe(
        probe,
    )

    observation["network"] = normalize_network(
        measurement,
        probe,
        result,
    )

    observation["location"] = normalize_location(
        probe,
    )

    observation["protocol"] = normalize_protocol(
        measurement,
        result,
    )

    observation["routing"] = normalize_routing(
        measurement,
        probe,
    )

    # observation["path"] = normalize_path()

    # observation["status"] = normalize_status(
    #     result,
    # )

    # observation["telemetry"] = normalize_telemetry(
    #     measurement,
    #     result,
    # )

    return observation