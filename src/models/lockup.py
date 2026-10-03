import uuid
import time
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class LockupStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
    EXPIRED = "EXPIRED"


class SecurityLockupEvent(BaseModel):
    lockup_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    triggered_at: float = Field(default_factory=time.time)
    trigger_reason: str = Field(..., description="Pattern type or fallback reason")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    locked_account_digests: List[str] = Field(default_factory=list)
    isolated_ip_hashes: List[str] = Field(default_factory=list)
    status: LockupStatus = Field(default=LockupStatus.ACTIVE)
