"""
============================================================
Project : DNS Measurement Platform
Script  : viewer.py

Description
-----------
Display SQLite archive data in JSON format.

Author
------
Helen Liu
============================================================
"""

import argparse
import json

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_reader import (
    get_all_measurements,
    get_all_probes,
    get_all_observations,
)


def clean_row(row, raw=False):
    """
    Convert SQLite row to display format.
    """

    item = dict(row)

    if not raw:
        item.pop("raw_json", None)

    else:

        if "raw_json" in item and item["raw_json"]:

            try:
                item["raw_json"] = json.loads(item["raw_json"])

            except Exception:
                pass

    json_fields = [
        "identity",
        "metadata",
        "network",
        "address_family",
        "location",
        "protocol",
        "routing",
        "path",
        "telemetry",
    ]

    for field in json_fields:

        if field in item and item[field]:

            try:

                item[field] = json.loads(item[field])

            except Exception:
                pass

    return item

def print_json(rows, raw=False):
    """
    Pretty print rows.
    """

    output = []

    for row in rows:

        output.append(
            clean_row(
                row,
                raw,
            )
        )

    print(
        json.dumps(
            output,
            indent=4,
            ensure_ascii=False,
        )
    )


def main():

    parser = argparse.ArgumentParser(
        description="SQLite Archive Viewer"
    )

    parser.add_argument(
        "--table",
        choices=[
            "measurement",
            "probe",
            "observation",
        ],
        help="View an entire table.",
    )

    parser.add_argument(
        "--latest",
        action="store_true",
        help="View latest observations.",
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="Display all fields including raw JSON.",
    )
    args = parser.parse_args()

    connection = get_connection()

    try:

        if args.table == "measurement":

            rows = get_all_measurements(connection)

            print_json(rows, raw=args.raw)

        elif args.table == "probe":

            rows = get_all_probes(connection)

            print_json(rows, raw=args.raw)

        elif args.table == "observation":

            rows = get_all_observations(connection)

            print_json(rows, raw=args.raw)

        elif args.latest:

            rows = get_all_observations(
                connection,
                limit=1,
            )

            print_json(rows, raw=args.raw)

        else:

            parser.print_help()

    finally:

        close_connection(connection)


if __name__ == "__main__":

    main()