"""
Test sqlite_reader.get_observation()
"""

from app.database.sqlite_connection import (
    get_connection,
    close_connection,
)

from app.database.sqlite_schema import (
    create_tables,
)

from app.database.sqlite_writer import (
    insert_observation,
)

from app.database.sqlite_reader import (
    get_observation,
)


def test_get_observation(db_connection):

    # connection = get_connection(
    #     "test_west_africa_dns.db"
    # )

    # create_tables(connection)

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
        db_connection,
        observation,
    )

    db_connection.commit()

    row = get_observation(
        db_connection,
        observation["identity"]["observation_id"],
    )

    #
    # Basic checks
    #

    assert row is not None

    #
    # JSON restore
    #

    assert isinstance(row["identity"], dict)
    assert isinstance(row["metadata"], dict)
    assert isinstance(row["network"], dict)
    assert isinstance(row["address_family"], dict)
    assert isinstance(row["location"], dict)
    assert isinstance(row["protocol"], dict)
    assert isinstance(row["routing"], dict)
    assert isinstance(row["path"], dict)
    assert isinstance(row["telemetry"], dict)

    #
    # Identity
    #

    assert (
        row["identity"]["observation_id"]
        == observation["identity"]["observation_id"]
    )

    assert (
        row["identity"]["measurement_id"]
        == observation["identity"]["measurement_id"]
    )

    assert (
        row["identity"]["probe_id"]
        == observation["identity"]["probe_id"]
    )

    #
    # Metadata
    #

    assert (
        row["metadata"]["observation_type"]
        == "DNS"
    )

    #
    # Protocol
    #

    assert (
        row["protocol"]["query_name"]
        == "youtube.com"
    )

    assert (
        row["protocol"]["rcode"]
        == "NOERROR"
    )

    # close_connection(connection)