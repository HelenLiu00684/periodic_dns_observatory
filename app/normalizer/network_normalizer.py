"""
============================================================
Project : DNS Measurement Platform
Module  : network_normalizer.py

Description
-----------
Normalizes the Network section of the Canonical
Observation.

The Network section stores protocol-independent network
facts generated during one Observation.

The structure follows the network protocol stack rather
than any application protocol.

Network is divided into four logical components:

    ip
    socket
    transport
    performance

This design allows the same Observation model to support
future DNS, HTTP, HTTPS, BGP, MQTT, QUIC and other
protocols without structural changes.

Author
------
Helen Liu
============================================================
"""

from typing import Any

from app.common.json_utils import (
    safe_dict,
    safe_float,
    safe_int,
)


# ==========================================================
# Public API
# ==========================================================

def normalize_network(
    measurement: dict[str, Any],
    probe: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the Network section of one Observation.
    """

    dns_result = safe_dict(
        result.get("result")
    )

    ip_version = safe_int(
        result.get(
            "af",
            measurement.get("af"),
        )
    )

    network = {

        "ip": _normalize_ip(
            ip_version,
            probe,
            result,
        ),

        "socket": _normalize_socket(
            result,
        ),

        "transport": _normalize_transport(
            result,
        ),

        "performance": _normalize_performance(
            dns_result,
        ),
    }

    return network


# ==========================================================
# IP
# ==========================================================

def _normalize_ip(
    ip_version: int | None,
    probe: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize IP layer information.
    """

    ip = {

        "ip_version": ip_version,

        "source_ipv4": None,

        "source_ipv6": None,

        "destination_ipv4": None,

        "destination_ipv6": None,
    }

    if ip_version == 4:

        ip["source_ipv4"] = probe.get(
            "address_v4"
        )

        ip["destination_ipv4"] = result.get(
            "dst_addr"
        )

    elif ip_version == 6:

        ip["source_ipv6"] = probe.get(
            "address_v6"
        )

        ip["destination_ipv6"] = result.get(
            "dst_addr"
        )

    return ip


# ==========================================================
# Socket
# ==========================================================

def _normalize_socket(
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize socket layer information.

    RIPE Atlas currently exposes only the destination port.

    Source port is reserved for future protocols.
    """

    return {

        "source_port": None,

        "destination_port": safe_int(
            result.get(
                "dst_port"
            )
        ),
    }


# ==========================================================
# Transport
# ==========================================================

def _normalize_transport(
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize transport layer information.
    """

    return {

        "protocol": result.get(
            "proto"
        ),
    }


# ==========================================================
# Performance
# ==========================================================

def _normalize_performance(
    dns_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize runtime performance metrics.
    """

    return {

        "response_time_ms": safe_float(
            dns_result.get(
                "rt"
            )
        ),
    }