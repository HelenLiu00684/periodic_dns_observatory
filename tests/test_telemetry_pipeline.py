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


def test_process_batch():

    connection = get_connection()

    metrics = process_batch(
        connection=connection,
        last_timestamp=0,
        batch_size=10,
    )

    assert metrics is not None

    assert isinstance(metrics, list)

    assert len(metrics) > 0

    assert len(metrics) % 4 == 0

    connection.close()