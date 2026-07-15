"""
============================================================
Project : DNS Measurement Platform
Module  : protocol_normalizer.py

Description
-----------
Normalizes the Protocol section of the Canonical
Observation.

This module acts as the Protocol Dispatcher.

It identifies the application protocol associated with the
current Observation, retrieves the corresponding protocol
definition from the central Protocol Registry, and delegates
protocol-specific decoding to the registered decoder.

The Protocol Normalizer contains no DNS-specific, HTTP-
specific, or other protocol-specific parsing logic.

Canonical Protocol Structure
----------------------------

The normalized Protocol section follows this structure:

    protocol

        name

        display_name

        family

        version

        decoded

Example:

    {
        "name": "dns",
        "display_name": "Domain Name System",
        "family": "application",
        "version": "RFC1035",
        "decoded": {
            ...
        }
    }

Design Principle
----------------
The Protocol Normalizer depends only on the Protocol
Registry.

Supporting a new protocol requires:

    1. Implementing a protocol decoder.

    2. Registering its metadata and decoder in registry.py.

No protocol-specific changes are required in this module.

This module does not:

    - Parse DNS packets
    - Decode protocol fields directly
    - Create Observation objects
    - Generate telemetry metrics
    - Perform database operations
    - Validate protocol payloads

Author
------
Helen Liu
============================================================
"""

from typing import Any

from app.protocol.registry import get_protocol


# ==========================================================
# Public API
# ==========================================================

def normalize_protocol(
    measurement: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the Protocol section of one Observation.

    Parameters
    ----------
    measurement : dict[str, Any]
        Measurement metadata containing the configured
        protocol type.

    result : dict[str, Any]
        Runtime measurement result passed to the registered
        protocol decoder.

    Returns
    -------
    dict[str, Any]
        Canonical Protocol section.

    Notes
    -----
    The Measurement type is the preferred source for the
    protocol name.

    The runtime Result type is used as a fallback when the
    Measurement does not provide one.
    """

    protocol_name = _get_protocol_name(
        measurement=measurement,
        result=result,
    )

    protocol_info = get_protocol(
        protocol_name
    )

    if protocol_info is None:
        return _create_unsupported_protocol(
            protocol_name
        )

    decoder = protocol_info.get(
        "decoder"
    )

    if not callable(decoder):
        return _create_unsupported_protocol(
            protocol_name
        )

    decoded_data = decoder(
        result
    )

    return {
        "name": protocol_name,
        "display_name": protocol_info.get(
            "display_name"
        ),
        "family": protocol_info.get(
            "family"
        ),
        "version": protocol_info.get(
            "version"
        ),
        "decoded": decoded_data,
    }


# ==========================================================
# Protocol Name
# ==========================================================

def _get_protocol_name(
    measurement: dict[str, Any],
    result: dict[str, Any],
) -> str:
    """
    Determine the normalized protocol name.

    Resolution Order
    ----------------
    1. Measurement type
    2. Runtime Result type
    3. Empty string

    Returns
    -------
    str
        Lowercase protocol name.
    """

    protocol_name = measurement.get(
        "type"
    )

    if protocol_name is None:
        protocol_name = result.get(
            "type"
        )

    if protocol_name is None:
        return ""

    return str(
        protocol_name
    ).strip().lower()


# ==========================================================
# Unsupported Protocol
# ==========================================================

def _create_unsupported_protocol(
    protocol_name: str,
) -> dict[str, Any]:
    """
    Create the canonical structure for an unsupported or
    unregistered protocol.

    The Protocol section keeps the detected protocol name,
    while registry metadata and decoded content remain empty.

    This preserves the Canonical Observation structure
    without introducing protocol-specific assumptions.
    """

    return {
        "name": protocol_name,
        "display_name": None,
        "family": None,
        "version": None,
        "decoded": None,
    }