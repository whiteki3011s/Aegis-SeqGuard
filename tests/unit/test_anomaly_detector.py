import time
from src.models.telemetry import RawTelemetryInput
from src.services.anonymizer import TelemetryAnonymizer
from src.services.anomaly_detector import AIAnomalyDetector


def test_normal_traffic_low_score():
    anonymizer = TelemetryAnonymizer()
    detector = AIAnomalyDetector(anomaly_threshold=0.75)

    # Random traffic across different IPs with non-sequential timing
    raw_entries = [
        RawTelemetryInput(account_identifier="user_x", ip_address="1.1.1.1", char_length=8, timestamp=time.time() - 500),
        RawTelemetryInput(account_identifier="user_m", ip_address="2.2.2.2", char_length=12, timestamp=time.time() - 300),
        RawTelemetryInput(account_identifier="user_a", ip_address="3.3.3.3", char_length=15, timestamp=time.time() - 100)
    ]
    digests = [anonymizer.anonymize(r) for r in raw_entries]

    window, trigger_type = detector.evaluate_window(digests)
    assert window.ordered_pattern_score < 0.75
    assert not window.is_anomalous
    assert trigger_type == "AI_PATTERN_ANALYSIS"


def test_ordered_sequential_attack_high_score():
    anonymizer = TelemetryAnonymizer()
    detector = AIAnomalyDetector(anomaly_threshold=0.75)

    # Dictionary attack: ordered target accounts from single IP signature with constant time delta
    base_time = time.time()
    attack_accounts = ["account_aaa", "account_aab", "account_aac", "account_aad", "account_aae"]
    raw_entries = [
        RawTelemetryInput(
            account_identifier=acct,
            ip_address="198.51.100.42",
            char_length=10,
            timestamp=base_time + idx * 0.1
        )
        for idx, acct in enumerate(attack_accounts)
    ]
    digests = [anonymizer.anonymize(r) for r in raw_entries]

    window, trigger_type = detector.evaluate_window(digests)
    assert window.ordered_pattern_score >= 0.75
    assert window.is_anomalous


def test_circuit_breaker_timeout_fallback():
    anonymizer = TelemetryAnonymizer()
    detector = AIAnomalyDetector(anomaly_threshold=0.75)

    raw_entries = [
        RawTelemetryInput(account_identifier=f"user_{i}", ip_address="10.0.0.1", char_length=8, timestamp=time.time() + i*0.01)
        for i in range(6)
    ]
    digests = [anonymizer.anonymize(r) for r in raw_entries]

    window, trigger_type = detector.evaluate_window(digests, simulate_timeout=True)
    assert window.is_anomalous
    assert trigger_type == "DETERMINISTIC_BURST_FALLBACK"
