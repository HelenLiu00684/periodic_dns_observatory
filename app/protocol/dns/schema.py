"""
============================================================
Project : DNS Measurement Platform
Module  : schema.py

Description
-----------
Defines the Canonical DNS Protocol Schema used by the
Network Observation Platform.

The schema defines the normalized fields stored for one
DNS protocol observation.

The schema contains field definitions only.

It does not perform:

    - Packet parsing
    - DNS decoding
    - Validation
    - Observation normalization
    - Telemetry generation
    - Database operations

Design Principle
----------------
The Canonical DNS Protocol object remains independent of:

    - RIPE Atlas
    - dnspython
    - SQLite
    - InfluxDB
    - Prometheus
    - Grafana

The DNS Packet Parser may use an internally structured
packet model.

The DNS Decoder converts that packet model into this
canonical flat protocol object.

Author
------
Helen Liu
============================================================
"""


# ==========================================================
# DNS Protocol Schema
#
# Logical DNS packet structure:
#
#     Header
#         transaction_id
#         flags
#         opcode
#         rcode
#
#     Question
#         query_name
#         query_type
#         query_class
#
#     Answer
#         answer_count
#         answers
#         ttl
#
#     Authority
#         authority_count
#         authority
#
#     Additional
#         additional_count
#         additional
#
#     Raw Packet
#         packet_size
#         raw_abuf
# ==========================================================

DNS_PROTOCOL_SCHEMA = [

    # ======================================================
    # Header
    # ======================================================

    "transaction_id",
    "flags",
    "opcode",
    "rcode",

    # ======================================================
    # Question
    # ======================================================

    "query_name",
    "query_type",
    "query_class",

    # ======================================================
    # Answer
    # ======================================================

    "answer_count",
    "answers",
    "ttl",

    # ======================================================
    # Authority
    # ======================================================

    "authority_count",
    "authority",

    # ======================================================
    # Additional
    # ======================================================

    "additional_count",
    "additional",

    # ======================================================
    # Raw Packet
    # ======================================================

    "packet_size",
    "raw_abuf",
]