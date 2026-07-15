"""
============================================================
Project : DNS Measurement Platform
Module  : telemetry_pipeline.py

Description
-----------
Telemetry processing pipeline.

Responsibilities
----------------
✓ Read Observations from SQLite

✓ Build Telemetry Metrics

Author
------
Helen Liu
============================================================
"""

from app.database.sqlite_connection import (
    get_connection,
)

from app.telemetry.telemetry_pipeline import (
    process_batch,
)


def test_process_batch(db_connection):


    result = process_batch(
        connection=db_connection,
        last_timestamp=0,
        batch_size=10,
    )

    #
    # Verify batch result.
    #

    assert result is not None

    assert isinstance(result, dict)

    #
    # Verify batch statistics.
    #

    assert result["observation_count"] > 0

    assert result["metric_count"] > 0

    assert result["written_count"] > 0

    #
    # Every Observation generates four metrics.
    #

    assert (
        result["metric_count"]
        == result["observation_count"] * 4
    )

    #
    # All generated metrics should be written.
    #

    assert (
        result["written_count"]
        == result["metric_count"]
    )

    #
    # Verify checkpoint.
    #

    assert result["last_timestamp"] > 0

  