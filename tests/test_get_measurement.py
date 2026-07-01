"""
Test sqlite_reader.get_measurement()
"""

from app.database.sqlite_connection import get_connection, close_connection
from app.database.sqlite_schema import create_tables
from app.database.sqlite_writer import insert_measurement
from app.database.sqlite_reader import get_measurement


def test_get_measurement(db_connection):

    # connection = get_connection("test_west_africa_dns.db")

    # create_tables(connection)

    measurement = {
        "id": 12345,
        "description": "Pytest Measurement",
        "target": "8.8.8.8",
        "interval": 900,
        "type": "dns",
        "af": 4,
        "start_time": 1719000000,
        "stop_time": 1719003600,
    }

    insert_measurement(db_connection, measurement)
    db_connection.commit()

    row = get_measurement(db_connection, measurement["id"],)

    assert row is not None
    assert row["measurement_id"] == measurement["id"]
    assert row["description"] == measurement["description"]
    assert row["target"] == measurement["target"]
    assert row["protocol"] == measurement["type"]
    assert row["interval_seconds"] == measurement["interval"]
    assert row["address_family"] == measurement["af"]
    assert row["start_time"] == measurement["start_time"]
    assert row["stop_time"] == measurement["stop_time"]

    # close_connection(connection)