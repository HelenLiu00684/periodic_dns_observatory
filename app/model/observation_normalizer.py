"""
============================================================
Project : DNS Measurement Platform
Module  : observation_normalizer.py

Description
-----------
Normalizes raw RIPE Atlas DNS measurement data into the
Canonical Observation Framework.

This module combines:

    - Measurement Metadata
    - Probe Metadata
    - Raw DNS Measurement Result

into one standardized Observation object.

Author
------
Helen Liu
============================================================
"""

from typing import Dict

from app.model.observation import create_empty_observation
from app.protocol.dns.decoder import decode_dns_result


# ==========================================================
# Public Function
# NOTE
# ----
# Functions prefixed with "_" are considered private helper
# functions in Python.
#
# They are intended to be used only inside this module.
#
# The only public API of this module is:
#
#     normalize_dns_observation()
# ==========================================================
# ==========================================================
# NOTE
# ----
# Dict is a Python type hint.
#
# JSON objects loaded with json.load() become Python
# dictionaries (dict).
#
# Example
#
# measurement["id"]
# probe["country_code"]
# ==========================================================
def normalize_dns_observation(
    measurement: Dict,
    probe: Dict,
    result: Dict,
) -> Dict:
    """
    Normalize one RIPE Atlas DNS result into one Observation.
    """

    observation = create_empty_observation()


    observation["identity"] = _normalize_identity(
        measurement,
        result,
    )

    observation["metadata"] = _normalize_metadata(
        measurement,
        result,
    )

    observation["network"] = _normalize_network(
        result,
    )

    observation["address_family"] = _normalize_address_family(
        result,
    )

    observation["location"] = _normalize_location(
        probe,
    )
    observation["protocol"] = decode_dns_result(
        result,
    )

    observation["routing"] = _normalize_routing()

    observation["path"] = _normalize_path()

    observation["telemetry"] = _normalize_telemetry(
        measurement,
        result,
    )

    return observation


# ==========================================================
# Identity
# NOTE
# ----
# dict.get() safely retrieves a value from a dictionary.
#
# Unlike:
#
#     result["dst_addr"]
#
# get() returns None instead of raising KeyError when the
# field does not exist.
#
# This makes the parser more tolerant of incomplete data.
# ==========================================================

def _normalize_identity(
    measurement: Dict,
    result: Dict,
) -> Dict:
    """
    Normalize platform-level identity fields.
    """

    measurement_id = measurement.get("id")
    probe_id = result.get("prb_id")
    timestamp = result.get("timestamp")

    observation_id = (
        f"dns-{measurement_id}-{probe_id}-{timestamp}"
    )

    return {
        "observation_id": observation_id,
        "measurement_id": measurement_id,
        "probe_id": probe_id,
    }


# ==========================================================
# Metadata
# ==========================================================

def _normalize_metadata(
    measurement: Dict,
    result: Dict,
) -> Dict:
    """
    Normalize general observation metadata.
    """

    return {
        "timestamp": result.get("timestamp"),
        "stored_timestamp": result.get("stored_timestamp"),
        "observation_type": "DNS",
        "measurement_name": result.get(
            "msm_name",
            measurement.get("description"),
        ),
    }


# ==========================================================
# Network
# ==========================================================

def _normalize_network(
    result: Dict,
) -> Dict:
    """
    Normalize network / transport-layer information.
    """

    dns_result = result.get("result", {})

    return {
        "resolver_ip": result.get("dst_addr"),
        "destination_port": _safe_int(result.get("dst_port")),
        "transport_protocol": result.get("proto"),
        "response_time": dns_result.get("rt"),
    }


# ==========================================================
# Address Family
# ==========================================================

def _normalize_address_family(
    result: Dict,
) -> Dict:
    """
    Normalize IPv4 / IPv6 information.
    """

    af = result.get("af")

    address_family = {
        "ip_version": af,
        "source_ipv4": None,
        "source_ipv6": None,
        "destination_ipv4": None,
        "destination_ipv6": None,
        "public_source_ip": result.get("from"),
    }

    if af == 4:
        address_family["source_ipv4"] = result.get("src_addr")
        address_family["destination_ipv4"] = result.get("dst_addr")

    elif af == 6:
        address_family["source_ipv6"] = result.get("src_addr")
        address_family["destination_ipv6"] = result.get("dst_addr")

    return address_family


# ==========================================================
# Location
# ==========================================================

def _normalize_location(
    probe: Dict,
) -> Dict:
    """
    Normalize probe location information.
    """

    geometry = probe.get("geometry", {})
    coordinates = geometry.get("coordinates", [])

    longitude = None
    latitude = None

    if isinstance(coordinates, list) and len(coordinates) == 2:
        longitude = coordinates[0]
        latitude = coordinates[1]

    return {
        "asn": probe.get("asn_v4"),
        "country": probe.get("country_code"),
        "latitude": latitude,
        "longitude": longitude,
        "probe_description": probe.get("description"),
    }



# ==========================================================
# Routing
# ==========================================================

def _normalize_routing() -> Dict:
    """
    Routing is reserved for RouteViews / RIPE RIS Live
    correlation.

    Current DNS-only observations do not populate this section.
    """

    return {
        "prefix": None,
        "origin_as": None,
        "next_hop": None,
        "as_path": None,
        "local_preference": None,
        "med": None,
        "communities": None,
    }


# ==========================================================
# Path
# ==========================================================

def _normalize_path() -> Dict:
    """
    Path is reserved for Traceroute correlation.

    Current DNS-only observations do not populate this section.
    """

    return {
        "hop_count": None,
        "hop_list": None,
        "hop_ip": None,
        "hop_latency": None,
        "hop_as": None,
    }


# ==========================================================
# Telemetry
# ==========================================================

def _normalize_telemetry(
    measurement: Dict,
    result: Dict,
) -> Dict:
    """
    Normalize telemetry collection metadata.
    """

    return {
        "collector": "RIPE Atlas",
        "collector_version": result.get("mver"),
        "platform": "RIPE Atlas",
        "sampling_interval": measurement.get("interval"),
        "collection_time": result.get("timestamp"),
        "storage_timestamp": result.get("stored_timestamp"),
    }


# ==========================================================
# DNS Packet Parser
# NOTE
# ----
# Optional[str] means this value may be either:
#
#     str
#
# or
#
#     None
#
# This is commonly used for optional JSON fields.
# ==========================================================




# ==========================================================
# Utility
# ==========================================================

def _safe_int(value):
    """
    Convert a value to int safely.
    """

    try:
        return int(value)

    except (TypeError, ValueError):
        return None