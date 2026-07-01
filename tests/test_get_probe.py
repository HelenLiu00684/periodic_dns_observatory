"""
Test sqlite_reader.get_probe()
"""

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_schema import (
    create_tables,
)

from app.database.sqlite_writer import (
    insert_probe,
)

from app.database.sqlite_reader import (
    get_probe,
)


def test_get_probe(db_connection):

    # connection = get_connection(
    #     "test_west_africa_dns.db"
    # )

    # create_tables(connection)

    probe = {
        "id": 1001,
        "asn_v4": 64512,
        "asn_v6": None,
        "country_code": "NG",
        "latitude": 9.0820,
        "longitude": 8.6753,
        "description": "Pytest Probe",
        "address_v4": "192.0.2.1",
        "address_v6": None,
        "prefix_v4": "192.0.2.0/24",
        "prefix_v6": None,
        "first_connected": 1719000000,
        "status_name": "Connected",
    }

    insert_probe(
        db_connection,
        probe,
    )

    db_connection.commit()

    row = get_probe(
        db_connection,
        1001,
    )

    assert row is not None

    assert row["probe_id"] == probe["id"]
    assert row["asn_v4"] == probe["asn_v4"]
    assert row["asn_v6"] == probe["asn_v6"]
    assert row["country_code"] == probe["country_code"]
    assert row["latitude"] == probe["latitude"]
    assert row["longitude"] == probe["longitude"]
    assert row["description"] == probe["description"]
    assert row["address_v4"] == probe["address_v4"]
    assert row["address_v6"] == probe["address_v6"]
    assert row["prefix_v4"] == probe["prefix_v4"]
    assert row["prefix_v6"] == probe["prefix_v6"]
    assert row["first_connected"] == probe["first_connected"]
    assert row["status_name"] == probe["status_name"]

    # close_connection(connection)