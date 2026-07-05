"""
============================================================
Project : DNS Measurement Platform
Module  : observations.py

Description
-----------
Observation Collection REST API.

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
    list_observations,
)

router = APIRouter(
    prefix="/observations",
    tags=["Observations"],
)


@router.get("")
def observations():
    """
    Return all Observations.
    """

    connection = get_connection()

    try:

        return list_observations(connection)

    finally:

        close_connection(connection)