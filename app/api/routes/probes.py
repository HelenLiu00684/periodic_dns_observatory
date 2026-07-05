"""
============================================================
Project : DNS Measurement Platform
Module  : probes.py

Description
-----------
Probe Collection REST API.

Author
------
Helen Liu
============================================================
"""

from fastapi import APIRouter

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_reader import (
    get_all_probes,
)

router = APIRouter(
    prefix="/probes",
    tags=["Probes"],
)


@router.get("")
def probes():
    """
    Return all Probes.
    """

    connection = get_connection()

    try:

        return get_all_probes(connection)

    finally:

        close_connection(connection)