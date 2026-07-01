import json
import base64
from collections import Counter

import dns.message


RESULT_FILE = "data/raw/results.json"


def load_results():

    with open(RESULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_answer_count(results):
    counter = Counter()

    skipped = 0

    for record in results:

        result = record.get("result", {})

        if "abuf" not in result:
            skipped += 1
            continue

        try:
            packet = base64.b64decode(result["abuf"])
            message = dns.message.from_wire(packet)

            answer_count = 0

            for rrset in message.answer:
                answer_count += len(rrset)

            counter[answer_count] += 1

        except Exception as e:
            skipped += 1

    print("\n========== DNS Response Profile ==========\n")

    total = sum(counter.values())

    for k in sorted(counter.keys()):
        print(f"{k:2d} Answer(s): {counter[k]}")

    print(f"\nDecoded : {total}")
    print(f"Skipped : {skipped}")

def main():

    results = load_results()

    analyze_answer_count(results)


if __name__ == "__main__":
    main()