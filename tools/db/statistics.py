"""
============================================================
Project : DNS Measurement Platform
Script  : statistics.py

Description
-----------
Display SQLite archive database summary.

Author
------
Helen Liu
============================================================
"""

import os

from datetime import (
    datetime,
    UTC,
)

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_reader import (
    get_database_summary,
)


# ==========================================================
# Helper
# ==========================================================

def epoch_to_utc(epoch: int) -> str:
    """
    Convert UNIX epoch timestamp to UTC string.
    """

    return datetime.fromtimestamp(
        epoch,
        UTC,
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Display SQLite archive summary.
    """

    connection = get_connection()

    try:

        db_path = "data/dns_measurement.db"

        db_size = os.path.getsize(
            db_path,
        )

        db_size_mb = db_size / (1024 * 1024)

        summary = get_database_summary(
            connection,
        )

        duration_seconds = (
            summary["latest_timestamp"]
            - summary["oldest_timestamp"]
        )

        duration_hours = (
            duration_seconds / 3600
        )

        print("=" * 60)
        print("West Africa DNS Observatory")
        print("SQLite Database Summary")
        print("=" * 60)

        print()

        print("Database File")
        print("-" * 60)
        print(db_path)

        print()

        print("Database Size")
        print("-" * 60)
        print(f"{db_size_mb:.2f} MB")

        print()

        print("Measurement ID")
        print("-" * 60)
        print(summary["latest_measurement"])

        print()

        print("Measurement Records")
        print("-" * 60)
        print(summary["measurement_count"])

        print()

        print("Probe Count")
        print("-" * 60)
        print(summary["probe_count"])

        print()

        print("Observation Count")
        print("-" * 60)
        print(summary["observation_count"])

        print()

        print("Collection Duration")
        print("-" * 60)
        print(f"Seconds : {duration_seconds}")
        print(f"Hours   : {duration_hours:.2f}")

        print()

        print("Oldest Observation")
        print("-" * 60)
        print(
            f"Epoch : {summary['oldest_timestamp']}"
        )
        print(
            f"UTC   : {epoch_to_utc(summary['oldest_timestamp'])}"
        )

        print()

        print("Latest Observation")
        print("-" * 60)
        print(
            f"Epoch : {summary['latest_timestamp']}"
        )
        print(
            f"UTC   : {epoch_to_utc(summary['latest_timestamp'])}"
        )

        print()
        print("=" * 60)

    finally:

        close_connection(
            connection,
        )


if __name__ == "__main__":

    main()