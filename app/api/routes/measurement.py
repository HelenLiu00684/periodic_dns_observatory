"""
============================================================
Project : DNS Measurement Platform
Module  : measurement.py

Description
-----------
Measurement REST API.

Single Measurement.

Author
------
Helen Liu
============================================================
"""

from fastapi import APIRouter, HTTPException

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_reader import (
    get_measurement,
)

router = APIRouter(
    prefix="/measurement",
    tags=["Measurement"],
)


@router.get("/{measurement_id}")
def measurement(
    measurement_id: int,
):
    """
    Return one Measurement.
    """

    connection = get_connection()

    try:

        measurement = get_measurement(
            connection,
            measurement_id,
        )

        if measurement is None:

            raise HTTPException(
                status_code=404,
                detail="Measurement not found.",
            )

        return measurement

    finally:

        close_connection(connection)