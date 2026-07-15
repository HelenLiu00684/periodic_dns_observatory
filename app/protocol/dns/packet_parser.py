"""
============================================================
Project : DNS Measurement Platform
Module  : packet_parser.py

Description
-----------
Parses a RIPE Atlas Base64-encoded DNS response packet into
a structured DNS Packet Model.

RIPE Atlas stores the original DNS response packet in the
result.abuf field.

Parsing Flow
------------

    Base64 abuf
        -> Binary DNS packet
        -> dnspython Message
        -> Structured DNS Packet Model

The parser returns the following logical sections:

    - header
    - question
    - answer
    - authority
    - additional

This module performs DNS packet parsing only.

It does not know about:

    - Canonical Observation
    - Measurement metadata
    - Probe metadata
    - SQLite
    - Telemetry
    - Grafana

The DNS Decoder is responsible for converting the
structured packet model into the Canonical DNS Protocol
object.

Author
------
Helen Liu
============================================================
"""

import base64
import logging
from typing import Any

import dns.flags
import dns.message
import dns.opcode
import dns.rcode
import dns.rdataclass
import dns.rdatatype


logger = logging.getLogger(__name__)


# ==========================================================
# Public API
# ==========================================================

def parse_dns_abuf(
    abuf: str | None,
) -> dict[str, dict[str, Any]]:
    """
    Parse a Base64-encoded RIPE Atlas DNS response packet.

    Parameters
    ----------
    abuf : str | None
        Base64-encoded DNS response packet.

    Returns
    -------
    dict[str, dict[str, Any]]
        Structured DNS Packet Model.

    Notes
    -----
    Invalid or missing packet data returns an empty packet
    model rather than raising an exception.

    Parsing failures are logged for later debugging.
    """

    parsed_packet = _create_empty_packet_model()

    if not abuf:
        return parsed_packet

    try:
        packet = base64.b64decode(
            abuf,
            validate=True,
        )

        message = dns.message.from_wire(
            packet,
        )

        parsed_packet["header"] = _parse_header(
            message
        )

        parsed_packet["question"] = _parse_question(
            message
        )

        parsed_packet["answer"] = _parse_answer(
            message
        )

        parsed_packet["authority"] = _parse_authority(
            message
        )

        parsed_packet["additional"] = _parse_additional(
            message
        )

    except Exception as error:
        logger.warning(
            "Unable to parse DNS abuf: %s",
            error,
        )

    return parsed_packet


# ==========================================================
# Empty Packet Model
# ==========================================================

def _create_empty_packet_model(
) -> dict[str, dict[str, Any]]:
    """
    Create an empty structured DNS Packet Model.
    """

    return {

        "header": {
            "transaction_id": None,
            "flags": None,
            "opcode": None,
            "rcode": None,
        },

        "question": {
            "query_name": None,
            "query_type": None,
            "query_class": None,
        },

        "answer": {
            "answer_count": 0,
            "answers": [],
            "ttl": None,
        },

        "authority": {
            "authority_count": 0,
            "authority": [],
        },

        "additional": {
            "additional_count": 0,
            "additional": [],
        },
    }


# ==========================================================
# Header
# ==========================================================

def _parse_header(
    message: dns.message.Message,
) -> dict[str, Any]:
    """
    Parse the DNS Header section.
    """

    return {
        "transaction_id": message.id,

        "flags": dns.flags.to_text(
            message.flags
        ),

        "opcode": dns.opcode.to_text(
            message.opcode()
        ),

        "rcode": dns.rcode.to_text(
            message.rcode()
        ),
    }


# ==========================================================
# Question
# ==========================================================

def _parse_question(
    message: dns.message.Message,
) -> dict[str, Any]:
    """
    Parse the first DNS Question section entry.

    RIPE Atlas DNS measurements normally contain one
    question.
    """

    question_data = {
        "query_name": None,
        "query_type": None,
        "query_class": None,
    }

    if not message.question:
        return question_data

    question = message.question[0]

    question_data["query_name"] = str(
        question.name
    ).rstrip(".")

    question_data["query_type"] = dns.rdatatype.to_text(
        question.rdtype
    )

    question_data["query_class"] = dns.rdataclass.to_text(
        question.rdclass
    )

    return question_data


# ==========================================================
# Answer
# ==========================================================

def _parse_answer(
    message: dns.message.Message,
) -> dict[str, Any]:
    """
    Parse the DNS Answer section.

    All record types are preserved as structured records.

    A and AAAA records also include an address field.
    """

    answers: list[dict[str, Any]] = []
    ttl_values: list[int] = []

    for rrset in message.answer:
        ttl_values.append(
            rrset.ttl
        )

        answers.extend(
            _parse_rrset(rrset)
        )

    return {
        "answer_count": len(answers),
        "answers": answers,

        # The minimum TTL is retained because it represents
        # the earliest cache-expiration boundary among the
        # returned answer records.
        "ttl": min(ttl_values) if ttl_values else None,
    }


# ==========================================================
# Authority
# ==========================================================

def _parse_authority(
    message: dns.message.Message,
) -> dict[str, Any]:
    """
    Parse the DNS Authority section.
    """

    authority_records: list[dict[str, Any]] = []

    for rrset in message.authority:
        authority_records.extend(
            _parse_rrset(rrset)
        )

    return {
        "authority_count": len(authority_records),
        "authority": authority_records,
    }


# ==========================================================
# Additional
# ==========================================================

def _parse_additional(
    message: dns.message.Message,
) -> dict[str, Any]:
    """
    Parse the DNS Additional section.

    dnspython represents EDNS OPT information separately
    from normal resource records.

    Normal additional records are preserved here.
    """

    additional_records: list[dict[str, Any]] = []

    for rrset in message.additional:
        additional_records.extend(
            _parse_rrset(rrset)
        )

    return {
        "additional_count": len(additional_records),
        "additional": additional_records,
    }


# ==========================================================
# Resource Record Set
# ==========================================================

def _parse_rrset(
    rrset: Any,
) -> list[dict[str, Any]]:
    """
    Convert one dnspython RRset into canonical dictionaries.
    """

    records: list[dict[str, Any]] = []

    record_type = dns.rdatatype.to_text(
        rrset.rdtype
    )

    record_class = dns.rdataclass.to_text(
        rrset.rdclass
    )

    record_name = str(
        rrset.name
    ).rstrip(".")

    for record in rrset:
        parsed_record = {
            "name": record_name,
            "type": record_type,
            "class": record_class,
            "ttl": rrset.ttl,
            "value": record.to_text(),
        }

        if rrset.rdtype in (
            dns.rdatatype.A,
            dns.rdatatype.AAAA,
        ):
            parsed_record["address"] = record.address

        records.append(
            parsed_record
        )

    return records