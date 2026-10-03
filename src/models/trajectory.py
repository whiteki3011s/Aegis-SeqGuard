import uuid
import time
from typing import List

from pydantic import BaseModel, Field
from src.models.telemetry import AuthenticationEntryDigest


class SequenceTrajectoryWindow(BaseModel):
    window_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = Field(default_factory=time.time)
    end_time: float = Field(default_factory=time.time)
    entries: List[AuthenticationEntryDigest] = Field(default_factory=list)
    ordered_pattern_score: float = Field(0.0, ge=0.0, le=1.0)
    is_anomalous: bool = Field(False)
