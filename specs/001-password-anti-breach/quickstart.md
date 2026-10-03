# Quickstart Validation Guide: AI Password Anti-Breaching System

## Scenario 1: Normal Authentication Traffic Simulation
Validate that standard, non-ordered login attempts process without triggering false-positive lockouts.

```bash
# Run pytest unit test suite for normal telemetry ingestion
pytest tests/unit/test_anomaly_detector.py -k "test_normal_traffic"
```

## Scenario 2: Ordered Breach Attack Simulation (Alphabetical / Dictionary Sequence)
Validate that submitting a rapid sequence of attempts in dictionary order triggers an automated security lockup in under 500ms.

```bash
# Run integration test verifying sequential attack lockout
pytest tests/integration/test_sequential_attack.py
```

## Scenario 3: AI Fail-Safe Circuit Breaker Timeout
Validate that artificial latency injected into the AI analyzer triggers deterministic backup lockup rules.

```bash
pytest tests/unit/test_circuit_breaker.py
```
