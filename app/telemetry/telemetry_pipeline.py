"""
============================================================
Project : DNS Measurement Platform
Module  : telemetry_pipeline.py

Description
-----------
Telemetry processing pipeline.

Responsibilities
----------------
✓ Read new Observations from SQLite

✓ Build Telemetry Metrics

✓ Return generated Metrics

Future
------
✓ Write Metrics into InfluxDB

✓ Update checkpoint

✓ Statistics

Author
------
Helen Liu
============================================================
"""

from sqlite3 import Connection
from typing import Dict, List

from app.database.sqlite_reader import (
    get_observations_after,
)

from app.telemetry.telemetry_builder import (
    build_metrics,
)

# from app.telemetry.influx_writer import (
#     write_metrics,
# )
# ==========================================================
# Telemetry Pipeline
# ==========================================================

def process_batch(
    connection: Connection,
    last_timestamp: int,
    batch_size: int = 1000,
) -> List[Dict]:
    """
    Process a batch of new Observations.

    Parameters
    ----------
    connection : Connection
        SQLite connection.

    last_timestamp : int
        Process observations newer than this timestamp.

    batch_size : int
        Maximum observations to process.

    Returns
    -------
    List[Dict]
        Generated Telemetry Metrics.
    """

    observations = get_observations_after(
        connection=connection,
        last_timestamp=last_timestamp,
        limit=batch_size,
    )

    metrics = []

    for observation in observations:

        metrics.extend(

            build_metrics(
                observation,
            )

        )

    return metrics
    # written = write_metrics(
    #     metrics,
    # )

    # return written