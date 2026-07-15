"""
============================================================
Project : DNS Measurement Platform
Module  : decoder.py

Description
-----------
Decodes one RIPE Atlas DNS measurement result into the
Canonical DNS Protocol object.

The decoder coordinates:

    - DNS Protocol Factory
    - DNS Packet Parser
    - RIPE Atlas runtime DNS fields

Decoder Flow
------------

    RIPE Atlas Result
        -> Extract result.abuf
        -> Parse DNS Packet Model
        -> Create Canonical DNS Protocol object
        -> Merge parsed DNS sections
        -> Preserve raw packet information
        -> Return Canonical DNS Protocol

This module is an orchestrator.

It does not implement DNS wire-format parsing.

The decoder does not know about:

    - Observation
    - Probe
    - Measurement normalization
    - SQLite
    - Telemetry
    - Grafana

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

from .factory import create_dns_protocol
from .packet_parser import parse_dns_abuf

from pprint import pprint




# ==========================================================
# Public API
# ==========================================================

def decode_dns_result(
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Decode one RIPE Atlas DNS result into the Canonical DNS
    Protocol object.

    Parameters
    ----------
    result : dict[str, Any]
        One RIPE Atlas DNS runtime result.

    Returns
    -------
    dict[str, Any]
        Canonical DNS Protocol object.

    Notes
    -----
    RIPE Atlas DNS results may contain either:

        result
            Successful DNS runtime data.

    or:

        error
            Timeout or collection failure information.

    When no successful DNS result exists, the function
    returns an empty Canonical DNS Protocol object.
    """

    protocol = create_dns_protocol()

    dns_result = safe_dict(
        result.get("result")
    )

    # ------------------------------------------------------
    # RIPE Atlas Timeout / Runtime Error
    # ------------------------------------------------------
    #
    # Failed RIPE Atlas observations may contain:
    #
    #     "error": {
    #         "timeout": 5000
    #     }
    #
    # In this case there is no DNS response packet and
    # therefore no abuf to decode.
    #
    # Observation execution status is normalized separately
    # by the Status Normalizer.
    # ------------------------------------------------------

    if not dns_result:
        return protocol

    raw_abuf = dns_result.get(
        "abuf"
    )

    parsed_packet = parse_dns_abuf(
        raw_abuf
    )

    _merge_packet_sections(
        protocol=protocol,
        parsed_packet=parsed_packet,
    )

    _apply_ripe_atlas_header_fallbacks(
        protocol=protocol,
        dns_result=dns_result,
    )

    protocol["packet_size"] = safe_int(
        dns_result.get("size")
    )

    protocol["raw_abuf"] = raw_abuf

    return protocol


# ==========================================================
# Packet Section Merge
# ==========================================================

def _merge_packet_sections(
    protocol: dict[str, Any],
    parsed_packet: dict[str, dict[str, Any]],
) -> None:
    """
    Merge structured DNS Packet Model sections into the
    flat Canonical DNS Protocol object.

    Unknown parser fields are ignored so the decoder remains
    compatible with the DNS Protocol Schema.
    """

    for section in parsed_packet.values():

        if not isinstance(section, dict):
            continue

        for field, value in section.items():

            if field in protocol:
                protocol[field] = value


# ==========================================================
# RIPE Atlas Fallbacks
# ==========================================================

def _apply_ripe_atlas_header_fallbacks(
    protocol: dict[str, Any],
    dns_result: dict[str, Any],
) -> None:
    """
    Apply header and count values supplied directly by RIPE
    Atlas when packet parsing did not provide them.

    RIPE Atlas commonly provides:

        ID
        QDCOUNT
        ANCOUNT
        NSCOUNT
        ARCOUNT

    The original DNS packet remains the preferred source.

    RIPE Atlas values act as reliable fallbacks for malformed
    or unavailable abuf data.
    """

    fallback_fields = {

        "transaction_id": safe_int(
            dns_result.get("ID")
        ),

        "answer_count": safe_int(
            dns_result.get("ANCOUNT")
        ),

        "authority_count": safe_int(
            dns_result.get("NSCOUNT")
        ),

        "additional_count": safe_int(
            dns_result.get("ARCOUNT")
        ),
    }

    for field, fallback_value in fallback_fields.items():

        current_value = protocol.get(
            field
        )

        if _is_missing_value(current_value):
            protocol[field] = fallback_value


# ==========================================================
# Missing Value
# ==========================================================

def _is_missing_value(
    value: Any,
) -> bool:
    """
    Determine whether a canonical field has no usable value.
    """

    return value is None