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

from typing import Dict, List, Optional
import base64

import dns.message
import dns.rcode
import dns.rdatatype

from app.model.observation import create_empty_observation


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

    observation["protocol"] = _normalize_dns_protocol(
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
# DNS Protocol
# ==========================================================

def _normalize_dns_protocol(
    result: Dict,
) -> Dict:
    """
    Normalize DNS protocol-specific information.
    """

    dns_result = result.get("result", {})
    parsed_dns = _parse_dns_abuf(
        dns_result.get("abuf")
    )

    return {
        "query_name": parsed_dns.get("query_name"),
        "query_type": parsed_dns.get("query_type"),
        "rcode": parsed_dns.get("rcode"),
        "ttl": parsed_dns.get("ttl"),
        "answer_count": parsed_dns.get("answer_count"),
        "answers": parsed_dns.get("answers"),
        "packet_size": dns_result.get("size"),
        "raw_abuf": dns_result.get("abuf"),
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

def _parse_dns_abuf(
    abuf: Optional[str],
) -> Dict:
    """
    Decode RIPE Atlas DNS abuf into DNS protocol fields.
    """

    parsed = {
        "query_name": None,
        "query_type": None,
        "rcode": None,
        "ttl": None,
        "answer_count": 0,
        "answers": [],
    }

    if not abuf:
        return parsed

    try:
# ==========================================================
# RIPE Atlas stores DNS packets as Base64 strings.
#
# Decode the Base64 string back into the original
# binary DNS packet.

# =============================================================================
# DNS Packet Example (RIPE Atlas)
#
# Original Base64 Packet (abuf)
#
# ciKBgAABAAEAAAABB3lvdXR1YmUDY29tAAABAAHADAABAAEAAADLAASs2RCOAAApEAAAAAAAAAA=
#
# After Base64 Decoding
#
# 72 22 81 80 00 01 00 01 00 00 00 01
# 07 79 6f 75 74 75 62 65
# 03 63 6f 6d
# 00
# 00 01
# 00 01
# c0 0c
# 00 01
# 00 01
# 00 00 00 cb
# 00 04
# ac d9 10 8e
# 00 00
# 29
# 10 00
# 00 00
# 00 00
# 00 00
#
#
# =============================================================================
# Packet Mapping
# =============================================================================
#
# Raw Bytes                 DNS Field                  Meaning
# -----------------------------------------------------------------------------
#
# 72 22                     Transaction ID             29218
#
#                                                    Unique identifier assigned
#                                                    by the client.
#                                                    The DNS response must
#                                                    contain the same ID.
#
# -----------------------------------------------------------------------------
#
# 81 80                     Flags                      QR RD RA
#
#                                                    QR = Query Response
#                                                         This packet is a DNS
#                                                         response.
#
#                                                    RD = Recursion Desired
#                                                         Client requests the
#                                                         resolver to perform
#                                                         recursive lookup.
#
#                                                    RA = Recursion Available
#                                                         Resolver supports
#                                                         recursive DNS service.
#
# -----------------------------------------------------------------------------
#
# 00 01                     Question Count            1
#
#                                                    One DNS question exists.
#
# -----------------------------------------------------------------------------
#
# 00 01                     Answer Count              1
#
#                                                    One answer record returned.
#
# -----------------------------------------------------------------------------
#
# 00 00                     Authority Count           0
#
#                                                    No authority records.
#
# -----------------------------------------------------------------------------
#
# 00 01                     Additional Count          1
#
#                                                    One EDNS OPT record.
#
# -----------------------------------------------------------------------------
#
# 07                         Label Length             7
#
#                                                    Next label contains
#                                                    7 characters.
#
# -----------------------------------------------------------------------------
#
# 79 6f 75 74 75 62 65      Domain Label              "youtube"
#
# -----------------------------------------------------------------------------
#
# 03                         Label Length             3
#
#                                                    Next label contains
#                                                    3 characters.
#
# -----------------------------------------------------------------------------
#
# 63 6f 6d                  Domain Label              "com"
#
# -----------------------------------------------------------------------------
#
# 00                         End of Name
#
#                                                    End of domain name.
#
# -----------------------------------------------------------------------------
#
# 00 01                     QTYPE                     A
#
#                                                    IPv4 Address Record.
#
# -----------------------------------------------------------------------------
#
# 00 01                     QCLASS                    IN
#
#                                                    Internet Class.
#
# -----------------------------------------------------------------------------
#
# c0 0c                     Name Pointer
#
#                                                    DNS Name Compression.
#
#                                                    Pointer to the domain
#                                                    name "youtube.com"
#                                                    stored in the Question
#                                                    section.
#
# -----------------------------------------------------------------------------
#
# 00 01                     TYPE                      A
#
#                                                    IPv4 Address Record.
#
# -----------------------------------------------------------------------------
#
# 00 01                     CLASS                     IN
#
#                                                    Internet Class.
#
# -----------------------------------------------------------------------------
#
# 00 00 00 cb               TTL                       203 seconds
#
#                                                    Resolver may cache this
#                                                    answer for 203 seconds.
#
# -----------------------------------------------------------------------------
#
# 00 04                     RDLENGTH                  4 bytes
#
#                                                    IPv4 address length.
#
# -----------------------------------------------------------------------------
#
# ac d9 10 8e               RDATA                     172.217.16.142
#
#                                                    Returned IPv4 address.
#
# -----------------------------------------------------------------------------
#
# 00 00                     OPT Name                 Root Label
#
# -----------------------------------------------------------------------------
#
# 29                         TYPE                     OPT (EDNS)
#
#                                                    Extension Mechanism
#                                                    for DNS (RFC 6891).
#
# -----------------------------------------------------------------------------
#
# 10 00                     UDP Payload Size          4096 bytes
#
#                                                    Maximum UDP payload
#                                                    supported by the client.
#
# -----------------------------------------------------------------------------
#
# 00 00                     Extended RCODE
#                            EDNS Version
#
#                                                    Extended RCODE = 0
#                                                    EDNS Version = 0
#
# -----------------------------------------------------------------------------
#
# 00 00                     Z Flags
#
#                                                    Reserved.
#
# -----------------------------------------------------------------------------
#
# 00 00                     Option Length
#
#                                                    No EDNS options.
#
# =============================================================================
# ==========================================================

        packet = base64.b64decode(abuf)
        print("=" * 60)
        print(packet.hex(" "))
        print("=" * 60)
        message = dns.message.from_wire(packet)
        print(dir(message))

# =============================================================================
# dnspython Message Object
#
# message = dns.message.from_wire(packet)
#
# After parsing the raw DNS packet, dnspython creates a
# Message object with the following structure:
#
# message
# ├── id                = 29218
# ├── flags             = QR RD RA
# ├── opcode            = QUERY
# ├── rcode()           = NOERROR
# │
# ├── question
# │      └── [0]
# │             ├── name      = youtube.com.
# │             ├── rdtype    = A
# │             └── rdclass   = IN
# │
# ├── answer
# │      └── [0]
# │             ├── name      = youtube.com.
# │             ├── ttl       = 203
# │             ├── rdtype    = A
# │             ├── rdclass   = IN
# │             └── address   = 172.217.16.142
# │
# ├── authority
# │      └── []
# │
# └── additional
#        └── [0]
#               ├── type       = OPT
#               ├── edns       = 0
#               └── payload    = 4096
#
# =============================================================================        
        parsed["rcode"] = dns.rcode.to_text(
            message.rcode()
        )

        if message.question:
            question = message.question[0]

            parsed["query_name"] = str(
                question.name
            ).rstrip(".")

            parsed["query_type"] = dns.rdatatype.to_text(
                question.rdtype
            )

        answers: List[str] = []
        ttl_values: List[int] = []

        for rrset in message.answer:
            ttl_values.append(rrset.ttl)

            for item in rrset:
                if rrset.rdtype in (
                    dns.rdatatype.A,
                    dns.rdatatype.AAAA,
                ):
                    answers.append(item.address)

        parsed["answers"] = answers
        parsed["answer_count"] = len(answers)

        if ttl_values:
            parsed["ttl"] = ttl_values[0]

    except Exception:
        return parsed

    return parsed


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