"""
============================================================
Project : DNS Measurement Platform
Module  : observation.py

Description
-----------
Observation REST API.

Single Observation.

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
    get_observation,
)

router = APIRouter(
    prefix="/observation",
    tags=["Observation"],
)


@router.get("/{observation_id}")
def observation(
    observation_id: str,
):
    """
    Return one Observation.
    """

    connection = get_connection()

    try:

        observation = get_observation(
            connection,
            observation_id,
        )

        if observation is None:

            raise HTTPException(
                status_code=404,
                detail="Observation not found.",
            )

        return observation

    finally:

        close_connection(connection)