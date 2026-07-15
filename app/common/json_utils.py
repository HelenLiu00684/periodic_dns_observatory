"""
============================================================
Project : DNS Measurement Platform
Module  : json_utils.py

Description
-----------
Provides common JSON utility functions shared across the
DNS Measurement Platform.

This module centralizes generic JSON helper functions used
by multiple platform components, including:

    • Collector
    • Normalizer
    • Repository
    • Validation

The module intentionally contains only JSON-related helper
functions.

No business logic, normalization, protocol parsing,
database operations or telemetry generation are performed
here.

Design Principle
----------------
Functions placed in this module should:

    • Be independent of business logic

    • Be reusable by multiple platform modules

    • Be unrelated to DNS, Measurement, Probe,
      Observation or SQLite

Business-specific processing belongs in the corresponding
Normalizer modules.

Author
------
Helen Liu
============================================================
"""

import json
from pathlib import Path
from typing import Any

import requests


# ==========================================================
# JSON Download
# ==========================================================

def download_json(
    url: str,
) -> dict | list:
    """
    Download JSON data from an HTTP endpoint.

    Parameters
    ----------
    url : str
        REST API endpoint.

    Returns
    -------
    dict | list
        Parsed JSON response.

    Raises
    ------
    requests.RequestException
        Raised if the HTTP request fails.
    """

    print(f"[GET] {url}")

    response = requests.get(
        url,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Save JSON
# ==========================================================

def save_json(
    data: Any,
    filename: Path,
) -> None:
    """
    Save JSON data to a local file.
    """

    filename.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"Saving JSON: {filename.resolve()}")

    with filename.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
        )

    print(f"Saved JSON: {filename.resolve()}")


# ==========================================================
# Load JSON
# ==========================================================

def load_json(
    filename: Path,
) -> dict | list:
    """
    Load JSON data from a local file.
    """

    with filename.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ==========================================================
# Safe Integer
# ==========================================================

def safe_int(
    value: Any,
) -> int | None:
    """
    Safely convert a value to an integer.

    Returns
    -------
    int | None
    """

    try:
        return int(value)

    except (TypeError, ValueError):
        return None


# ==========================================================
# Safe Float
# ==========================================================

def safe_float(
    value: Any,
) -> float | None:
    """
    Safely convert a value to a float.

    Returns
    -------
    float | None
    """

    try:
        return float(value)

    except (TypeError, ValueError):
        return None


# ==========================================================
# Safe Dictionary
# ==========================================================

def safe_dict(
    value: Any,
) -> dict:
    """
    Return a dictionary.

    Returns an empty dictionary if the supplied value is not
    a dictionary.
    """

    if isinstance(value, dict):
        return value

    return {}


# ==========================================================
# Safe List
# ==========================================================

def safe_list(
    value: Any,
) -> list:
    """
    Return a list.

    Returns an empty list if the supplied value is not a
    list.
    """

    if isinstance(value, list):
        return value

    return []


# ==========================================================
# Safe Boolean
# ==========================================================

def safe_bool(
    value: Any,
) -> bool | None:
    """
    Safely normalize a boolean value.

    Accepted values:

        True
        False
        "true"
        "false"
        "1"
        "0"
        1
        0
    """

    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value != 0

    if isinstance(value, str):

        value = value.strip().lower()

        if value in (
            "true",
            "1",
            "yes",
        ):
            return True

        if value in (
            "false",
            "0",
            "no",
        ):
            return False

    return None