"""
============================================================
Project : DNS Measurement Platform
Module  : measurements.py

Description
-----------
Measurement Collection REST API.

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
    get_all_measurements,
)

router = APIRouter(
    prefix="/measurements",
    tags=["Measurements"],
)


@router.get("")
def measurements():
    """
    Return all Measurements.
    """

    connection = get_connection()

    try:

        return get_all_measurements(connection)

    finally:

        close_connection(connection)