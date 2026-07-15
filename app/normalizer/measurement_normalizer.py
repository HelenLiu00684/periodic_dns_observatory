"""
============================================================
Project : DNS Measurement Platform
Module  : measurement_normalizer.py

Description
-----------
Normalizes the Measurement section of the Canonical
Observation.

Measurement describes the configuration used to perform
an Observation.

Measurement is configuration rather than runtime data.

One Measurement may generate thousands of Observations.

Author
------
Helen Liu
============================================================
"""

from typing import Any

from app.common.json_utils import (
    safe_dict,
    safe_int,
    safe_list,
)


# ==========================================================
# Public API
# ==========================================================

def normalize_measurement(
    measurement: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the Measurement section of one Observation.
    """

    status = safe_dict(
        measurement.get("status")
    )

    return {

        "definition": _normalize_definition(
            measurement,
        ),

        "schedule": _normalize_schedule(
            measurement,
        ),

        "network": _normalize_network(
            measurement,
        ),

        "dns": _normalize_dns(
            measurement,
        ),

        "target": _normalize_target(
            measurement,
        ),

        "probes": _normalize_probes(
            measurement,
        ),

        "status": {

            "id": safe_int(
                status.get("id")
            ),

            "name": status.get(
                "name"
            ),
        },

        "options": _normalize_options(
            measurement,
        ),
    }


# ==========================================================
# Definition
# ==========================================================

def _normalize_definition(
    measurement: dict[str, Any],
) -> dict[str, Any]:

    return {

        "description": measurement.get(
            "description"
        ),

        "measurement_type": measurement.get(
            "type"
        ),

        "group_id": safe_int(
            measurement.get("group_id")
        ),
    }


# ==========================================================
# Schedule
# ==========================================================

def _normalize_schedule(
    measurement: dict[str, Any],
) -> dict[str, Any]:

    return {

        "interval_seconds": safe_int(
            measurement.get("interval")
        ),

        "start_time": safe_int(
            measurement.get("start_time")
        ),

        "timeout_ms": safe_int(
            measurement.get("timeout")
        ),
    }


# ==========================================================
# Network
# ==========================================================

def _normalize_network(
    measurement: dict[str, Any],
) -> dict[str, Any]:

    return {

        "ip_version": safe_int(
            measurement.get("af")
        ),

        "transport_protocol": measurement.get(
            "protocol"
        ),

        "configured_destination_port": safe_int(
            measurement.get("port")
        ),
    }


# ==========================================================
# DNS
# ==========================================================

def _normalize_dns(
    measurement: dict[str, Any],
) -> dict[str, Any]:

    return {

        "question": {

            "query_name": measurement.get(
                "query_argument"
            ),

            "query_type": measurement.get(
                "query_type"
            ),

            "query_class": measurement.get(
                "query_class"
            ),
        },
    }


# ==========================================================
# Target
# ==========================================================

def _normalize_target(
    measurement: dict[str, Any],
) -> dict[str, Any]:

    return {

        "target_hostname": measurement.get(
            "target"
        ),

        "target_ip": measurement.get(
            "target_ip"
        ),

        "resolved_ips": safe_list(
            measurement.get(
                "resolved_ips"
            )
        ),

        "target_asn": safe_int(
            measurement.get(
                "target_asn"
            )
        ),

        "target_prefix": measurement.get(
            "target_prefix"
        ),
    }


# ==========================================================
# Probes
# ==========================================================

def _normalize_probes(
    measurement: dict[str, Any],
) -> dict[str, Any]:

    return {

        "probes_requested": safe_int(
            measurement.get(
                "probes_requested"
            )
        ),

        "probes_scheduled": safe_int(
            measurement.get(
                "probes_scheduled"
            )
        ),
    }


# ==========================================================
# Options
# ==========================================================

def _normalize_options(
    measurement: dict[str, Any],
) -> dict[str, Any]:

    return {

        "include_abuf": measurement.get(
            "include_abuf"
        ),

        "resolve_on_probe": measurement.get(
            "resolve_on_probe"
        ),

        "udp_payload_size": safe_int(
            measurement.get(
                "udp_payload_size"
            )
        ),
    }