from tests.helpers.loader import (
    load_measurement,
    load_probe,
    load_results,
)


def test_loader():

    measurement = load_measurement()

    assert measurement is not None

    results = load_results()

    assert len(results) > 0

    probe_id = results[0]["prb_id"]

    probe = load_probe(probe_id)

    assert probe is not None