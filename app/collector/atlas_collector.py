from measurement import fetch_measurement
from results import fetch_results
from probes import fetch_all_probes


def main():

    print("=" * 60)
    print("RIPE Atlas Collector")
    print("=" * 60)

    print("\nDownloading measurement metadata...")
    fetch_measurement()

    print("\nDownloading measurement results...")
    results = fetch_results()

    print("\nDownloading probe metadata...")
    fetch_all_probes(results)

    print("\nDone.")


if __name__ == "__main__":
    main()