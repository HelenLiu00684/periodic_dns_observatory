"""
============================================================
Project : DNS Measurement Platform
Module  : statistics.py

Description
-----------
Statistics REST API.

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

from app.database.sqlite_reader import get_statistics

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


@router.get("")
def statistics():
    """
    Return database statistics.
    """

    connection = get_connection()

    try:
        return get_statistics(connection)

    finally:
        close_connection(connection)