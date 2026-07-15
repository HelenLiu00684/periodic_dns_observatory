"""
============================================================
Project : DNS Measurement Platform
Module  : location_normalizer.py

Description
-----------
Normalizes the Location section of the Canonical
Observation.

The Location section stores only geographic information.

Routing information such as ASN and IP Prefixes does not
belong here and is normalized separately by the Routing
Normalizer.

Author
------
Helen Liu
============================================================
"""

from typing import Any

from app.common.json_utils import (
    safe_dict,
    safe_list,
)


# ==========================================================
# Public API
# ==========================================================

def normalize_location(
    probe: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the Location section of one Observation.
    """

    geometry = safe_dict(
        probe.get("geometry")
    )

    coordinates = safe_list(
        geometry.get("coordinates")
    )

    latitude = None
    longitude = None

    if len(coordinates) >= 2:

        longitude = coordinates[0]
        latitude = coordinates[1]

    return {

        "country": probe.get(
            "country_code"
        ),

        "latitude": latitude,

        "longitude": longitude,

        "geometry_type": geometry.get(
            "type"
        ),
    }