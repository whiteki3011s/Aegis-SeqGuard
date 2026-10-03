import json
import random
import time
import urllib.request
import urllib.error

API_URL = "http://127.0.0.1:8000/api/v1/telemetry/ingest"


def post_telemetry(payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_legit_user_simulation():
    # Single user attempting 5 passwords for their own account from home IP
    user_ip = f"198.51.100.{random.randint(10, 250)}"
    single_account = "legit_user_john_doe"

    print("=== AI Password Anti-Breach: Legitimate User Test ===")
    print(f"Targeting server: {API_URL}")
    print(f"User '{single_account}' trying 5 different passwords from IP: {user_ip}\n")

    base_time = time.time()

    # Human typing speeds (irregular gaps: 2.5s, 4.1s, 3.0s, 5.2s)
    human_delays = [0.0, 2.5, 6.6, 9.6, 14.8]

    for idx, delay in enumerate(human_delays):
        payload = {
            "account_identifier": single_account,
            "ip_address": user_ip,
            "char_length": 8 + (idx % 3),  # varying password length guesses
            "timestamp": base_time + delay
        }

        try:
            res = post_telemetry(payload)
            status = res.get("status")
            score = res.get("anomaly_score", "N/A")
            lockup = res.get("lockup_activated")

            print(f"Attempt {idx+1} (Single Account Retry): Status={status:<12} Anomaly Score={score:<6} Lockup={lockup}")
        except urllib.error.URLError as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
    run_legit_user_simulation()
