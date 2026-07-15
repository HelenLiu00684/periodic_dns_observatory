"""
============================================================
Project : DNS Measurement Platform
Module  : factory.py

Description
-----------
Creates an empty Canonical DNS Protocol object.

The factory is responsible only for object creation.

It initializes every field defined by the DNS Protocol
Schema to None.

The factory contains no protocol parsing, decoding,
validation, or business logic.

Design Principle
----------------

The DNS Factory guarantees that every DNS Observation
starts from the same canonical structure.

Author
------
Helen Liu
============================================================
"""

from typing import Any

from .schema import DNS_PROTOCOL_SCHEMA


# ==========================================================
# Public API
# ==========================================================

def create_dns_protocol() -> dict[str, Any]:
    """
    Create an empty Canonical DNS Protocol object.

    Returns
    -------
    dict[str, Any]

        Empty DNS protocol object with all schema fields
        initialized to None.
    """

    return {

        field: None

        for field in DNS_PROTOCOL_SCHEMA

    }