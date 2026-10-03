from src.models.telemetry import RawTelemetryInput
from src.services.anonymizer import TelemetryAnonymizer


def test_anonymize_basic():
    anonymizer = TelemetryAnonymizer()
    raw = RawTelemetryInput(
        account_identifier="alice_user",
        ip_address="192.168.1.50",
        char_length=12,
        user_agent="Mozilla/5.0"
    )
    digest = anonymizer.anonymize(raw)

    # Verify zero-plaintext: raw strings must NOT exist on digest object
    assert not hasattr(digest, "account_identifier")
    assert not hasattr(digest, "ip_address")

    # Verify HMAC hash output
    assert len(digest.account_digest) == 64
    assert len(digest.ip_hash) == 64
    assert digest.char_length_bucket == 16


def test_anonymize_determinism():
    anonymizer = TelemetryAnonymizer()
    raw1 = RawTelemetryInput(
        account_identifier="Bob_Smith",
        ip_address="10.0.0.1",
        char_length=8
    )
    raw2 = RawTelemetryInput(
        account_identifier="bob_smith ",
        ip_address="10.0.0.1",
        char_length=8
    )
    digest1 = anonymizer.anonymize(raw1)
    digest2 = anonymizer.anonymize(raw2)

    # Identical normalized inputs produce identical salted hashes
    assert digest1.account_digest == digest2.account_digest
    assert digest1.ip_hash == digest2.ip_hash
