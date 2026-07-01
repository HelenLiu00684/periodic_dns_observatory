from config import *
from utils import *


def fetch_probe(probe_id):

    url = f"{BASE_URL}/probes/{probe_id}/"

    data = get_json(url)

    save_json(
        data,
        PROBE_DIR / f"{probe_id}.json"
    )

    return data

def fetch_all_probes(results):

    probe_ids = sorted(
        set(
            item["prb_id"]
            for item in results
            if "prb_id" in item
        )
    )

    print(f"{len(probe_ids)} probes found.")

    for pid in probe_ids:

        try:

            fetch_probe(pid)

        except Exception as e:

            print(pid, e)