"""
============================================================
Project : DNS Measurement Platform

Test
----
Telemetry Builder

Author
------
Helen Liu
============================================================
"""

from app.telemetry.telemetry_builder import (
    build_metrics,
)

from app.telemetry.dns.types import (
    DNS_RESPONSE_TIME,
    DNS_PACKET_SIZE,
    DNS_ANSWER_COUNT,
    DNS_RCODE,
)


def test_build_dns_metrics():

    observation = {

        "identity": {
            "probe_id": 1015492,
        },

        "metadata": {
            "timestamp": 1783295009,
            "observation_type": "DNS",
        },

        "network": {
            "resolver_ip": "8.8.8.8",
            "response_time": 39.294,
        },

        "location": {
            "country": "LT",
        },

        "protocol": {
            "query_name": "youtube.com",
            "query_type": "A",
            "packet_size": 96,
            "answer_count": 1,
            "rcode": "NOERROR",
        },
    }

    metrics = build_metrics(
        observation,
    )

    #
    # Builder should generate four metrics.
    #

    assert len(metrics) == 4

    #
    # Verify measurements.
    #

    measurement_names = {

        metric["measurement"]

        for metric in metrics

    }

    assert DNS_RESPONSE_TIME in measurement_names

    assert DNS_PACKET_SIZE in measurement_names

    assert DNS_ANSWER_COUNT in measurement_names

    assert DNS_RCODE in measurement_names

    #
    # Verify Response Time Metric
    #

    response_metric = next(

        metric

        for metric in metrics

        if metric["measurement"] == DNS_RESPONSE_TIME

    )

    assert response_metric["tags"]["probe_id"] == 1015492

    assert response_metric["tags"]["country"] == "LT"

    assert response_metric["tags"]["resolver"] == "8.8.8.8"

    assert response_metric["tags"]["query_name"] == "youtube.com"

    assert response_metric["tags"]["query_type"] == "A"

    assert response_metric["fields"]["value"] == 39.294

    assert response_metric["timestamp"] == 1783295009

    #
    # Verify Packet Size
    #

    packet_metric = next(

        metric

        for metric in metrics

        if metric["measurement"] == DNS_PACKET_SIZE

    )

    assert packet_metric["fields"]["value"] == 96

    #
    # Verify Answer Count
    #

    answer_metric = next(

        metric

        for metric in metrics

        if metric["measurement"] == DNS_ANSWER_COUNT

    )

    assert answer_metric["fields"]["value"] == 1

    #
    # Verify RCODE
    #

    rcode_metric = next(

        metric

        for metric in metrics

        if metric["measurement"] == DNS_RCODE

    )

    assert rcode_metric["fields"]["value"] == "NOERROR"