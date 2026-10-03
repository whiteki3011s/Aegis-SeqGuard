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


def run_simulation():
    # Generate a random IP for each simulation run to test fresh attack detection
    random_octet = random.randint(10, 250)
    attack_ip = f"198.51.100.{random_octet}"
    target_accounts = [
        f"user_alpha_{random_octet}",
        f"user_beta_{random_octet}",
        f"user_gamma_{random_octet}",
        f"user_delta_{random_octet}",
        f"user_epsilon_{random_octet}"
    ]

    print("=== AI Password Anti-Breach Defense Test ===")
    print(f"Targeting server: {API_URL}")
    print(f"Simulating rapid attack sequence from fresh IP: {attack_ip}\n")

    base_time = time.time()

    for idx, account in enumerate(target_accounts):
        payload = {
            "account_identifier": account,
            "ip_address": attack_ip,
            "char_length": 8 + idx,
            "timestamp": base_time + (idx * 0.05)
        }

        try:
            res = post_telemetry(payload)
            status = res.get("status")
            score = res.get("anomaly_score", "N/A")
            lockup = res.get("lockup_activated")

            print(f"Attempt {idx+1} [Account: {account:<16}]: Status={status:<26} Anomaly Score={score} Lockup={lockup}")
        except urllib.error.URLError as e:
            print(f"Error connecting to server (is 'python src/main.py' running?): {e}")
            break


if __name__ == "__main__":
    run_simulation()
