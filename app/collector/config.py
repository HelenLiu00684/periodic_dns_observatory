from pathlib import Path

# Measurement
MEASUREMENT_ID = 186325158

# API
BASE_URL = "https://atlas.ripe.net/api/v2"

# Directories
DATA_DIR = Path("data")

RAW_DIR = DATA_DIR / "raw"
METADATA_DIR = DATA_DIR / "metadata"
PROBE_DIR = DATA_DIR / "probes"

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)
PROBE_DIR.mkdir(parents=True, exist_ok=True)