"""
============================================================
Project : DNS Measurement Platform
Module  : routing_normalizer.py

Description
-----------
Normalizes the Routing section of the Canonical
Observation.

The Routing section stores network routing information
associated with one Observation.

Current DNS observations contain routing inventory only.

Future BGP observations will populate routing path
attributes without changing the Observation model.

Author
------
Helen Liu
============================================================
"""

from typing import Any

from app.common.json_utils import (
    safe_int,
)


# ==========================================================
# Public API
# ==========================================================

def normalize_routing(
    measurement: dict[str, Any],
    probe: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the Routing section of one Observation.
    """

    return {

        "bgp": {

            "source": _normalize_source(
                probe,
            ),

            "destination": _normalize_destination(
                measurement,
            ),

            "path_attributes": _normalize_path_attributes(),
        },
    }


# ==========================================================
# Source
# ==========================================================

def _normalize_source(
    probe: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize source routing information.

    Source routing information comes from the Probe
    inventory.
    """

    return {

        "asn_v4": safe_int(
            probe.get(
                "asn_v4"
            )
        ),

        "asn_v6": safe_int(
            probe.get(
                "asn_v6"
            )
        ),

        "prefix_v4": probe.get(
            "prefix_v4"
        ),

        "prefix_v6": probe.get(
            "prefix_v6"
        ),
    }


# ==========================================================
# Destination
# ==========================================================

def _normalize_destination(
    measurement: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize destination routing information.

    Destination routing information comes from the
    Measurement definition.
    """

    af = safe_int(
        measurement.get("af")
    )

    destination = {

        "asn_v4": None,

        "asn_v6": None,

        "prefix_v4": None,

        "prefix_v6": None,
    }

    if af == 4:

        destination["asn_v4"] = safe_int(
            measurement.get(
                "target_asn"
            )
        )

        destination["prefix_v4"] = measurement.get(
            "target_prefix"
        )

    elif af == 6:

        destination["asn_v6"] = safe_int(
            measurement.get(
                "target_asn"
            )
        )

        destination["prefix_v6"] = measurement.get(
            "target_prefix"
        )

    return destination


# ==========================================================
# Path Attributes
# ==========================================================

def _normalize_path_attributes(
) -> dict[str, Any]:
    """
    Normalize BGP path attributes.

    DNS observations do not populate these fields.

    They are reserved for future BGP Routing Event
    observations.
    """

    return {

        "next_hop": None,

        "as_path": None,

        "communities": None,

        "local_preference": None,

        "med": None,
    }