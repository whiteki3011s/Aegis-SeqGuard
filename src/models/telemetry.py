import time
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class RawTelemetryInput(BaseModel):
    account_identifier: str = Field(..., description="Target username or account identifier")
    ip_address: str = Field(..., description="Source IP address")
    char_length: int = Field(..., ge=1, description="Password character length")
    user_agent: Optional[str] = Field("unknown", description="User-Agent or device fingerprint")
    timestamp: float = Field(default_factory=time.time, description="Attempt timestamp in seconds")


class AuthenticationEntryDigest(BaseModel):
    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    account_digest: str = Field(..., description="HMAC-SHA256 salted hash of account identifier")
    ip_hash: str = Field(..., description="HMAC-SHA256 salted hash of source IP")
    char_length_bucket: int = Field(..., ge=1, description="Categorized password character length")
    device_signature_hash: str = Field(..., description="HMAC-SHA256 hash of device signature")
