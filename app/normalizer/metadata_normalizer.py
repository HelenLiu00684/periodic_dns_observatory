"""
============================================================
Project : DNS Measurement Platform
Module  : metadata_normalizer.py

Description
-----------
Normalizes the Metadata section of the Canonical
Observation.

Metadata describes runtime information associated with one
Observation.

Metadata is independent of protocol-specific information
and contains only platform-level runtime metadata.

Author
------
Helen Liu
============================================================
"""

from typing import Any


# ==========================================================
# Public API
# ==========================================================

def normalize_metadata(
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the Metadata section of one Observation.
    """

    observation_type = _normalize_observation_type(
        result.get("type")
    )

    return {

        "timestamp": result.get(
            "timestamp"
        ),

        "stored_timestamp": result.get(
            "stored_timestamp"
        ),

        "observation_type": observation_type,

        "measurement_engine_version": result.get(
            "mver"
        ),

        "probe_firmware_version": result.get(
            "fw"
        ),
    }


# ==========================================================
# Private Functions
# ==========================================================

def _normalize_observation_type(
    observation_type: Any,
) -> str:
    """
    Normalize the Observation type.

    Example
    -------

    dns

        -> DNS

    traceroute

        -> TRACEROUTE

    bgp

        -> BGP
    """

    if observation_type is None:
        return "UNKNOWN"

    return str(observation_type).upper()