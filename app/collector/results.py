from config import *
from utils import *


def fetch_results():

    url = f"{BASE_URL}/measurements/{MEASUREMENT_ID}/results/"

    data = get_json(url)

    save_json(
        data,
        RAW_DIR / "results.json"
    )

    return data