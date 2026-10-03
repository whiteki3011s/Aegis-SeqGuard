import hmac
import hashlib
from src.models.telemetry import RawTelemetryInput, AuthenticationEntryDigest

SECRET_SALT = b"anti_breach_security_salt_2026"


class TelemetryAnonymizer:
    def __init__(self, salt: bytes = SECRET_SALT):
        self.salt = salt

    def _hash_value(self, value: str) -> str:
        return hmac.new(self.salt, value.encode('utf-8'), hashlib.sha256).hexdigest()

    def anonymize(self, raw: RawTelemetryInput) -> AuthenticationEntryDigest:
        account_digest = self._hash_value(raw.account_identifier.strip().lower())
        ip_hash = self._hash_value(raw.ip_address.strip())
        device_signature_hash = self._hash_value((raw.user_agent or "unknown").strip())

        # Bucketize character length
        if raw.char_length <= 6:
            length_bucket = 6
        elif raw.char_length <= 10:
            length_bucket = 10
        elif raw.char_length <= 16:
            length_bucket = 16
        else:
            length_bucket = 20

        return AuthenticationEntryDigest(
            timestamp=raw.timestamp,
            account_digest=account_digest,
            ip_hash=ip_hash,
            char_length_bucket=length_bucket,
            device_signature_hash=device_signature_hash
        )
