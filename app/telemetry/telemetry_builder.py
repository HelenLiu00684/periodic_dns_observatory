"""
============================================================
Project : DNS Measurement Platform
Module  : telemetry_builder.py

Description
-----------
Build telemetry metrics from Canonical Observation objects.

This module coordinates protocol-specific telemetry builders.

Author
------
Helen Liu
============================================================
"""

from typing import Dict, List

from app.telemetry.dns.metrics import (
    build_dns_metrics,
)


def build_metrics(
    observation: Dict,
) -> List[Dict]:
    """
    Build telemetry metrics from one Observation.
    """

    metrics = []

    observation_type = (
        observation
        .get("metadata", {})
        .get("observation_type")
    )

    if observation_type == "DNS":

        metrics.extend(
            build_dns_metrics(
                observation,
            )
        )

    return metrics