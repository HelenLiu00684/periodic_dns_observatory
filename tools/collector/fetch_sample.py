import requests
import json

MEASUREMENT_ID = 186325158

url = (
    f"https://atlas.ripe.net/api/v2/measurements/"
    f"{MEASUREMENT_ID}/results/"
)

response = requests.get(url)

print("Status Code:", response.status_code)

results = response.json()

print("Total records:", len(results))

print("\n=== First Record ===")
print(json.dumps(results[0], indent=4))