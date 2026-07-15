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
from typing import Dict, Any

from app.database.sqlite_reader import (
    get_observations_after,
)

from app.telemetry.telemetry_builder import (
    build_metrics,
)

from app.telemetry.influxdb.influx_writer import (
    write_metrics,
)
# ==========================================================
# Telemetry Pipeline
# ==========================================================
# Telemetry Processing Pipeline
#
# SQLite Observation
#          │
#          ▼
# SQLite Reader
#          │
#          ▼
# Canonical Observation
#          │
#          ▼
# Telemetry Builder
#          │
#          ▼
# Canonical Metrics
#          │
#          ▼
# Influx Writer
#          │
#          ▼
# InfluxDB Bucket
#
# ==========================================================

def process_batch(
    connection: Connection,
    last_timestamp: int,
    batch_size: int = 1000,
) -> Dict[str, Any]:
    """
    Process a batch of new Observations.
    Workflow

        SQLite
            ↓
        Observation
            ↓
        Canonical Metrics
            ↓
        InfluxDB
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
        Number of telemetry metrics
        successfully written into InfluxDB.
    """
    #
    # Step 1
    # Read new Observations from SQLite.
    #
    observations = get_observations_after(
        connection=connection,
        last_timestamp=last_timestamp,
        limit=batch_size,
    )
    #
    # Step 2
    # Convert every Observation into
    # Canonical Telemetry Metrics.
    #
    metrics = []

    for observation in observations:

        metrics.extend(

            build_metrics(
                observation,
            )

        )

    # return metrics
    # #
    # Step 3
    # Write all generated Metrics
    # into InfluxDB.
    #

    written_count = write_metrics(
        metrics,
    )
    #
    # Step 4
    # Determine the checkpoint timestamp.
    #
    if observations:

        next_timestamp = observations[-1]["metadata"]["timestamp"]

    else:

        next_timestamp = last_timestamp


    #
    # Step 5
    # Return batch processing result.
    #

    return {

        "observation_count": len(observations),

        "metric_count": len(metrics),

        "written_count": written_count,

        "last_timestamp": next_timestamp,

    }


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("Telemetry Pipeline Module")        