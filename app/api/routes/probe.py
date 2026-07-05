"""
============================================================
Project : DNS Measurement Platform
Module  : probe.py

Description
-----------
Probe REST API.

Single Probe.

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
    get_probe,
)

router = APIRouter(
    prefix="/probe",
    tags=["Probe"],
)


@router.get("/{probe_id}")
def probe(
    probe_id: int,
):
    """
    Return one Probe.
    """

    connection = get_connection()

    try:

        probe = get_probe(
            connection,
            probe_id,
        )

        if probe is None:

            raise HTTPException(
                status_code=404,
                detail="Probe not found.",
            )

        return probe

    finally:

        close_connection(connection)