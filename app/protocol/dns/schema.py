"""
DNS Protocol Schema

Defines the canonical DNS protocol fields used by
the Observation Framework.
"""

DNS_PROTOCOL_SCHEMA = [

    # DNS Header
    "transaction_id",
    "flags",
    "opcode",
    "rcode",

    # Question
    "query_name",
    "query_type",
    "query_class",

    # Answer
    "answer_count",
    "answers",
    "ttl",

    # Authority
    "authority_count",
    "authority",

    # Additional
    "additional_count",
    "additional",

    # Raw Packet
    "packet_size",
    "raw_abuf",
]