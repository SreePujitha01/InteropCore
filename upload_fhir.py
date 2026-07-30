import requests
import json
import os

FHIR_SERVER = "http://localhost:8080/fhir"
FHIR_DIR = "data/fhir"

headers = {"Content-Type": "application/fhir+json"}

def sort_key(filename):
    if "hospitalInformation" in filename:
        return (0, filename)
    if "practitionerInformation" in filename:
        return (1, filename)
    return (2, filename)

filenames = sorted(os.listdir(FHIR_DIR), key=sort_key)

success_count = 0
fail_count = 0

for filename in filenames:
    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(FHIR_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    try:
        response = requests.post(FHIR_SERVER, json=bundle, headers=headers, timeout=180)
        if response.status_code in (200, 201):
            success_count += 1
            print(f"Uploaded {filename}: {response.status_code}")
        else:
            fail_count += 1
            print(f"FAILED {filename}: {response.status_code} - {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        fail_count += 1
        print(f"ERROR {filename}: {type(e).__name__} - {e}")

print(f"\nDone. Success: {success_count}, Failed: {fail_count}")