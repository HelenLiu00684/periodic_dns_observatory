"""
============================================================
Project : DNS Measurement Platform
Module  : metrics.py

Description
-----------
DNS telemetry metric builder.

Each helper function creates one telemetry metric.

Author
------
Helen Liu
============================================================
"""

from typing import Dict, List

from app.telemetry.telemetry_models import (
    create_empty_metric,
)

from app.telemetry.dns.types import (
    DNS_RESPONSE_TIME,
    DNS_PACKET_SIZE,
    DNS_ANSWER_COUNT,
    DNS_RCODE,
)


# ==========================================================
# Public Function
# ==========================================================

def build_dns_metrics(
    observation: Dict,
) -> List[Dict]:
    """
    Build all DNS telemetry metrics.
    """

    metrics = []

    metrics.append(
        _build_response_time(
            observation,
        )
    )

    metrics.append(
        _build_packet_size(
            observation,
        )
    )

    metrics.append(
        _build_answer_count(
            observation,
        )
    )

    metrics.append(
        _build_rcode(
            observation,
        )
    )

    return metrics


# ==========================================================
# Common Metric
# ==========================================================

def _create_metric(
    measurement: str,
    observation: Dict,
) -> Dict:
    """
    Create a telemetry metric with common attributes.
    """

    metric = create_empty_metric()

    metric["measurement"] = measurement

    metric["tags"] = _build_tags(
        observation,
    )

    metric["timestamp"] = _build_timestamp(
        observation,
    )

    return metric


# ==========================================================
# Common Tags
# ==========================================================

def _build_tags(
    observation: Dict,
) -> Dict:
    """
    Build common telemetry tags.
    """

    return {

        "probe_id":
            observation["identity"]["probe_id"],

        "country":
            observation["location"]["country"],

        "resolver":
            observation["network"]["resolver_ip"],

        "query_name":
            observation["protocol"]["query_name"],

        "query_type":
            observation["protocol"]["query_type"],
    }


# ==========================================================
# Common Timestamp
# ==========================================================

def _build_timestamp(
    observation: Dict,
):
    """
    Build telemetry timestamp.
    """

    return observation["metadata"]["timestamp"]


# ==========================================================
# Response Time
# ==========================================================

def _build_response_time(
    observation: Dict,
) -> Dict:
    """
    Build DNS response time metric.
    """

    metric = _create_metric(
        DNS_RESPONSE_TIME,
        observation,
    )

    metric["fields"] = {

        "value":
            observation["network"]["response_time"],
    }

    return metric


# ==========================================================
# Packet Size
# ==========================================================

def _build_packet_size(
    observation: Dict,
) -> Dict:
    """
    Build DNS packet size metric.
    """

    metric = _create_metric(
        DNS_PACKET_SIZE,
        observation,
    )

    metric["fields"] = {

        "value":
            observation["protocol"]["packet_size"],
    }

    return metric


# ==========================================================
# Answer Count
# ==========================================================

def _build_answer_count(
    observation: Dict,
) -> Dict:
    """
    Build DNS answer count metric.
    """

    metric = _create_metric(
        DNS_ANSWER_COUNT,
        observation,
    )

    metric["fields"] = {

        "value":
            observation["protocol"]["answer_count"],
    }

    return metric


# ==========================================================
# RCODE
# ==========================================================

def _build_rcode(
    observation: Dict,
) -> Dict:
    """
    Build DNS response code metric.
    """

    metric = _create_metric(
        DNS_RCODE,
        observation,
    )

    metric["fields"] = {

        "value":
            observation["protocol"]["rcode"],
    }

    return metric