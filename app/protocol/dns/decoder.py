"""
============================================================
Project : DNS Measurement Platform
Module  : decoder.py

Description
-----------
Decodes one RIPE Atlas DNS measurement result into the
canonical DNS protocol object.

The decoder is responsible for:

    - Creating an empty DNS protocol object
    - Parsing the DNS packet
    - Populating protocol fields

The decoder does not know about Observation,
SQLite, FastAPI, or Telemetry.

Author
------
Helen Liu
============================================================
"""

from typing import Dict

from .factory import create_dns_protocol
from .packet_parser import parse_dns_abuf


def decode_dns_result(result: Dict) -> Dict:
    """
    Decode one RIPE Atlas DNS result into a DNS protocol object.
    """

    protocol = create_dns_protocol()

    dns_result = result.get("result", {})
    parsed_dns = parse_dns_abuf(
        dns_result.get("abuf")
    )

    protocol["query_name"] = parsed_dns.get("query_name")
    protocol["query_type"] = parsed_dns.get("query_type")
    protocol["rcode"] = parsed_dns.get("rcode")
    protocol["ttl"] = parsed_dns.get("ttl")
    protocol["answer_count"] = parsed_dns.get("answer_count")
    protocol["answers"] = parsed_dns.get("answers")

    protocol["packet_size"] = dns_result.get("size")
    protocol["raw_abuf"] = dns_result.get("abuf")

    return protocol