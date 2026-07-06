import json
import requests
from pathlib import Path


def save_json(data, filename):

    filename.parent.mkdir(parents=True, exist_ok=True)

    print("Saving to:", filename.resolve())

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Saved:", filename.resolve())


def get_json(url):

    print(f"[GET] {url}")

    r = requests.get(url, timeout=60)

    r.raise_for_status()

    return r.json()