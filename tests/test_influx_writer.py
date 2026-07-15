"""
============================================================
Project : DNS Measurement Platform

Test
----
InfluxDB Writer

Author
------
Helen Liu
============================================================
"""

from app.telemetry.influxdb.influx_writer import (
    write_metrics,
)

import time

def test_write_metrics():

    metrics = [

        {
            "measurement": "dns_response_time",

            "tags": {

                "probe_id": 1015492,

                "country": "LT",

                "resolver": "8.8.8.8",

                "query_name": "youtube.com",

                "query_type": "A",
            },

            "fields": {

                "value": 39.294,
            },

            "timestamp": int(time.time()),
        }

    ]

    written = write_metrics(
        metrics,
    )

    assert written == 1