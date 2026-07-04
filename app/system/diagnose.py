"""
============================================================
Project : DNS Measurement Platform
Module  : diagnose.py

Description
-----------
Platform diagnosis engine.

Author
------
Helen Liu
============================================================
"""

import argparse
import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def check(command: list[str]) -> bool:
    """
    Execute a command and return True if it succeeds.
    """

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def build_report():

    collector = check(
        ["./tools/collector/status.sh"]
    )

    database = check(
        ["./tools/db/status.sh"]
    )

    sqlite = check(
        ["./tools/db/health.sh"]
    )
    # Overall platform health requires all components
    # to pass their individual health checks.
    overall = all([
        collector,
        database,
        sqlite,
    ])

    return {
        "platform": "DNS Measurement Platform",
        "version": "1.0",

        "collector": {
            "status": "PASS" if collector else "FAIL"
        },

        "database": {
            "status": "PASS" if database else "FAIL"
        },

        "sqlite": {
            "status": "PASS" if sqlite else "FAIL"
        },

        "overall": {
            "status":
                "HEALTHY"
                if overall
                else "UNHEALTHY"
        },
    }


def print_human(report):

    print("=" * 60)
    print("DNS Measurement Platform")
    print("System Diagnosis")
    print("=" * 60)

    print()

    print("Collector")
    print("-" * 60)
    print(report["collector"]["status"])

    print()

    print("Database")
    print("-" * 60)
    print(report["database"]["status"])

    print()

    print("SQLite")
    print("-" * 60)
    print(report["sqlite"]["status"])

    print()

    print("Overall")
    print("-" * 60)
    print(report["overall"]["status"])

    print()
    print("=" * 60)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format.",
    )

    args = parser.parse_args()

    report = build_report()

    if args.json:

        print(
            json.dumps(
                report,
                indent=4,
            )
        )

    else:

        print_human(report)


if __name__ == "__main__":

    main()