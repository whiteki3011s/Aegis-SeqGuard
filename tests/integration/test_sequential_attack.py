import time
from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)


def test_sequential_attack_endpoint_flow():
    # 1. Ingest normal initial traffic
    resp = client.post("/api/v1/telemetry/ingest", json={
        "account_identifier": "user_alpha",
        "ip_address": "203.0.113.1",
        "char_length": 8,
        "timestamp": time.time() - 200
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "PROCESSED"
    assert not resp.json()["lockup_activated"]

    # 2. Simulate rapid ordered dictionary attack across multiple accounts from single IP
    base_time = time.time()
    attack_targets = ["dict_word_a", "dict_word_b", "dict_word_c", "dict_word_d", "dict_word_e"]

    activated_event = None
    for idx, target in enumerate(attack_targets):
        res = client.post("/api/v1/telemetry/ingest", json={
            "account_identifier": target,
            "ip_address": "198.51.100.99",
            "char_length": 10,
            "timestamp": base_time + idx * 0.05
        })
        if res.json().get("status") == "SECURITY_LOCKUP_ACTIVATED":
            activated_event = res.json()

    # The sequential pattern triggers automated security lockout
    assert activated_event is not None
    assert activated_event["lockup_activated"]
    lockup_id = activated_event["lockup_id"]

    # 3. Subsequent requests from locked vector are BLOCKED immediately
    blocked_resp = client.post("/api/v1/telemetry/ingest", json={
        "account_identifier": "dict_word_z",
        "ip_address": "198.51.100.99",
        "char_length": 10,
        "timestamp": time.time()
    })
    assert blocked_resp.json()["status"] == "BLOCKED"

    # 4. Resolve lockup via incident response API
    resolve_resp = client.post(f"/api/v1/lockup/resolve/{lockup_id}")
    assert resolve_resp.status_code == 200
    assert resolve_resp.json()["status"] == "RESOLVED"
