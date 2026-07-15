"""
============================================================
Project : Network Telemetry Platform
Module  : registry.py

Description
-----------
Central Protocol Registry.

The Protocol Registry maintains protocol metadata and
provides the corresponding protocol decoder.

The Observation Framework never communicates directly
with protocol implementations.

Instead, the Protocol Normalizer queries this registry
to obtain protocol information and the appropriate
protocol decoder.

Design Principle
----------------

This module follows the Open-Closed Principle.

Supporting a new protocol requires only:

    1. Implementing a protocol decoder.

    2. Registering the protocol metadata.

No modification to the Observation Framework is required.

Current Supported Protocols
---------------------------

    • DNS

Future Protocols
---------------------------

    • HTTP
    • HTTPS
    • SNMP
    • MQTT
    • NTP
    • gRPC

Author
------
Helen Liu
============================================================
"""

from collections.abc import Callable
from typing import Any

from app.protocol.dns.decoder import decode_dns_result


# ==========================================================
# Protocol Registry
# ==========================================================

PROTOCOL_REGISTRY: dict[
    str,
    dict[str, Any],
] = {

    # ======================================================
    # DNS
    # ======================================================

    "dns": {

        "display_name": "Domain Name System",

        "family": "application",

        "version": "RFC1035",

        "decoder": decode_dns_result,
    },

    # ======================================================
    # Future Protocols
    # ======================================================

    #
    # "http": {
    #
    #     "display_name": "Hypertext Transfer Protocol",
    #
    #     "family": "application",
    #
    #     "version": "RFC9110",
    #
    #     "decoder": decode_http_result,
    # },
    #
    # "snmp": {
    #
    #     "display_name": "Simple Network Management Protocol",
    #
    #     "family": "management",
    #
    #     "version": "RFC3416",
    #
    #     "decoder": decode_snmp_result,
    # },
}


# ==========================================================
# Public API
# ==========================================================

def get_protocol(
    protocol: str,
) -> dict[str, Any] | None:
    """
    Retrieve protocol metadata.

    Parameters
    ----------
    protocol

        Application protocol name.

    Returns
    -------
    dict | None

        Registered protocol information.
    """

    return PROTOCOL_REGISTRY.get(
        protocol.lower(),
    )


def get_protocol_decoder(
    protocol: str,
) -> Callable | None:
    """
    Retrieve the registered protocol decoder.
    """

    protocol_info = get_protocol(
        protocol,
    )

    if protocol_info is None:
        return None

    return protocol_info["decoder"]


def is_protocol_supported(
    protocol: str,
) -> bool:
    """
    Determine whether a protocol is supported.
    """

    return protocol.lower() in PROTOCOL_REGISTRY


def list_supported_protocols(
) -> list[str]:
    """
    Return all registered protocol names.
    """

    return sorted(
        PROTOCOL_REGISTRY.keys(),
    )