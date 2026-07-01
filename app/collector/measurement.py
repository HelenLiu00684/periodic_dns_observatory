from config import *
from utils import *


def fetch_measurement():

    url = f"{BASE_URL}/measurements/{MEASUREMENT_ID}/"

    data = get_json(url)

    save_json(
        data,
        METADATA_DIR / "measurement_metadata.json"
    )

    return data