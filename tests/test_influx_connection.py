"""
============================================================
Project : DNS Measurement Platform

Test
----
InfluxDB Connection

Author
------
Helen Liu
============================================================
"""

from app.telemetry.influxdb.influx_connection import (
    get_influx_client,
    close_influx_client,
)


def test_influx_connection():

    client = get_influx_client()

    #
    # Verify client creation.
    #

    assert client is not None

    #
    # Verify InfluxDB server is reachable.
    #

    assert client.ping() is True

    close_influx_client(client)