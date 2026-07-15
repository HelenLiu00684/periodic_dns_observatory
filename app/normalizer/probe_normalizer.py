"""
============================================================
Project : DNS Measurement Platform
Module  : probe_normalizer.py

Description
-----------
Normalizes the Probe section of the Canonical Observation.

Probe describes the inventory information of a RIPE Atlas
Probe.

Probe information is infrastructure metadata rather than
runtime observation data.

Address information, geographic information and routing
information are normalized into their own Observation
sections.

Author
------
Helen Liu
============================================================
"""

from typing import Any

from app.common.json_utils import (
    safe_dict,
    safe_int,
)


# ==========================================================
# Public API
# ==========================================================

def normalize_probe(
    probe: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the Probe section of one Observation.
    """

    status = safe_dict(
        probe.get("status")
    )

    return {

        "definition": _normalize_definition(
            probe,
        ),

        "lifecycle": _normalize_lifecycle(
            probe,
        ),

        "status": {

            "id": safe_int(
                status.get("id")
            ),

            "name": status.get(
                "name"
            ),

            "since": status.get(
                "since"
            ),

            "status_since": safe_int(
                probe.get(
                    "status_since"
                )
            ),
        },
    }


# ==========================================================
# Definition
# ==========================================================

def _normalize_definition(
    probe: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize Probe definition.
    """

    return {

        "probe_type": probe.get(
            "type"
        ),

        "description": probe.get(
            "description"
        ),

        "firmware_version": safe_int(
            probe.get(
                "firmware_version"
            )
        ),

        "is_anchor": probe.get(
            "is_anchor"
        ),
    }


# ==========================================================
# Lifecycle
# ==========================================================

def _normalize_lifecycle(
    probe: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize Probe lifecycle information.
    """

    return {

        "first_connected": safe_int(
            probe.get(
                "first_connected"
            )
        ),

        "last_connected": safe_int(
            probe.get(
                "last_connected"
            )
        ),

        "total_uptime": safe_int(
            probe.get(
                "total_uptime"
            )
        ),
    }