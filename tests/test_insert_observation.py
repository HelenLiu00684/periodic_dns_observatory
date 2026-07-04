"""
Test sqlite_writer.insert_observation()
"""

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)
from app.database.sqlite_schema import create_tables
from app.database.sqlite_writer import insert_observation


def test_insert_observation():

    connection = get_connection("dns_measurement.db")

    create_tables(connection)

    observation = {

        "identity": {
            "observation_id": "dns-12345-1001-1719000000",
            "measurement_id": 12345,
            "probe_id": 1001,
        },

        "metadata": {
            "timestamp": 1719000000,
            "stored_timestamp": 1719000010,
            "observation_type": "DNS",
            "measurement_name": "Pytest DNS",
        },

        "network": {
            "resolver_ip": "8.8.8.8",
            "destination_port": 53,
            "transport_protocol": "UDP",
            "response_time": 45.3,
        },

        "address_family": {
            "ip_version": 4,
            "source_ipv4": "192.0.2.1",
            "source_ipv6": None,
            "destination_ipv4": "8.8.8.8",
            "destination_ipv6": None,
            "public_source_ip": "198.51.100.10",
        },

        "location": {
            "asn": 64512,
            "country": "NG",
            "latitude": 9.0820,
            "longitude": 8.6753,
            "probe_description": "Pytest Probe",
        },

        "protocol": {
            "query_name": "youtube.com",
            "query_type": "A",
            "rcode": "NOERROR",
            "ttl": 300,
            "answer_count": 1,
            "answers": [
                "142.250.190.78",
            ],
            "packet_size": 96,
            "raw_abuf": "AAAA",
        },

        "routing": {
            "prefix": None,
            "origin_as": None,
            "next_hop": None,
            "as_path": None,
            "local_preference": None,
            "med": None,
            "communities": None,
        },

        "path": {
            "hop_count": None,
            "hop_list": None,
            "hop_ip": None,
            "hop_latency": None,
            "hop_as": None,
        },

        "telemetry": {
            "collector": "RIPE Atlas",
            "collector_version": "2.0",
            "platform": "RIPE Atlas",
            "sampling_interval": 900,
            "collection_time": 1719000000,
            "storage_timestamp": 1719000010,
        },
    }

    insert_observation(
        connection,
        observation,
    )

    connection.commit()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM observation
        WHERE observation_id = ?
        """,
        (
            observation["identity"]["observation_id"],
        ),
    )

    row = cursor.fetchone()

    assert row is not None

    assert row["observation_id"] == observation["identity"]["observation_id"]
    assert row["measurement_id"] == observation["identity"]["measurement_id"]
    assert row["probe_id"] == observation["identity"]["probe_id"]
    assert row["observation_type"] == observation["metadata"]["observation_type"]

    close_connection(connection)