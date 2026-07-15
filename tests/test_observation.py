from pathlib import Path
import json

from app.common.json_utils import load_json
from app.model.observation_normalizer import (
    normalize_dns_observation,
)

# ---------------------------------------------------------
# Load Collector Data
# ---------------------------------------------------------

measurement = load_json(
    Path(
        "data/collector/metadata/measurement_metadata.json"
    )
)

probe = load_json(
    Path(
        "data/collector/probes/1000082.json"
    )
)

results = load_json(
    Path(
        "data/collector/raw/results.json"
    )
)

# ---------------------------------------------------------
# Select One Successful DNS Observation
# ---------------------------------------------------------

result = next(
    (
        item
        for item in results
        if "result" in item
    ),
    None,
)

if result is None:
    raise RuntimeError(
        "No successful DNS result found."
    )

# ---------------------------------------------------------
# Normalize Observation
# ---------------------------------------------------------

observation = normalize_dns_observation(
    measurement,
    probe,
    result,
)

# ---------------------------------------------------------
# Print Observation
# ---------------------------------------------------------

print(
    json.dumps(
        observation,
        indent=4,
    )
)