import time
import math
from typing import List, Tuple
from src.models.telemetry import AuthenticationEntryDigest
from src.models.trajectory import SequenceTrajectoryWindow


class AIAnomalyDetector:
    def __init__(self, anomaly_threshold: float = 0.75, timeout_ms: float = 50.0):
        self.anomaly_threshold = anomaly_threshold
        self.timeout_ms = timeout_ms

    def _calculate_sequence_order_score(self, entries: List[AuthenticationEntryDigest]) -> float:
        if len(entries) < 3:
            return 0.0

        # Sort entries temporally
        sorted_entries = sorted(entries, key=lambda e: e.timestamp)
        
        # 1. Compute time delta consistency and attempt velocity
        time_deltas = [
            max(0.0001, sorted_entries[i].timestamp - sorted_entries[i-1].timestamp)
            for i in range(1, len(sorted_entries))
        ]
        mean_delta = sum(time_deltas) / len(time_deltas)
        delta_variance = sum((d - mean_delta) ** 2 for d in time_deltas) / len(time_deltas)
        time_regularity_score = max(0.0, 1.0 - math.sqrt(delta_variance) / (mean_delta + 1e-5))

        # Fast velocity burst score (< 2.0s between requests)
        velocity_score = max(0.0, min(1.0, 1.5 / (mean_delta + 0.1)))

        # 2. Account diversity & single-source isolation
        ip_hashes = set(e.ip_hash for e in sorted_entries)
        account_hashes = set(e.account_digest for e in sorted_entries)
        
        multi_account_ratio = len(account_hashes) / len(sorted_entries)
        same_source_ratio = 1.0 if len(ip_hashes) <= 2 else (1.0 / len(ip_hashes))

        # Composite risk score calculation
        composite_score = (
            0.45 * (multi_account_ratio * same_source_ratio) +
            0.35 * velocity_score +
            0.20 * time_regularity_score
        )

        return min(1.0, max(0.0, composite_score))

    def evaluate_window(
        self,
        entries: List[AuthenticationEntryDigest],
        simulate_timeout: bool = False
    ) -> Tuple[SequenceTrajectoryWindow, str]:
        start_time = time.time()
        
        # Circuit breaker / fallback check
        if simulate_timeout:
            # Deterministic hardcoded rule fallback
            fallback_score = 0.90 if len(entries) >= 5 else 0.0
            window = SequenceTrajectoryWindow(
                start_time=entries[0].timestamp if entries else time.time(),
                end_time=entries[-1].timestamp if entries else time.time(),
                entries=entries,
                ordered_pattern_score=fallback_score,
                is_anomalous=(fallback_score >= self.anomaly_threshold)
            )
            return window, "DETERMINISTIC_BURST_FALLBACK"

        try:
            score = self._calculate_sequence_order_score(entries)
            elapsed_ms = (time.time() - start_time) * 1000.0
            
            if elapsed_ms > self.timeout_ms:
                # Timeout trigger fallback
                fallback_score = 0.90 if len(entries) >= 5 else score
                window = SequenceTrajectoryWindow(
                    start_time=entries[0].timestamp if entries else time.time(),
                    end_time=entries[-1].timestamp if entries else time.time(),
                    entries=entries,
                    ordered_pattern_score=fallback_score,
                    is_anomalous=(fallback_score >= self.anomaly_threshold)
                )
                return window, "TIMEOUT_FALLBACK_TRIGGER"

            is_anomalous = (score >= self.anomaly_threshold)
            window = SequenceTrajectoryWindow(
                start_time=entries[0].timestamp if entries else time.time(),
                end_time=entries[-1].timestamp if entries else time.time(),
                entries=entries,
                ordered_pattern_score=score,
                is_anomalous=is_anomalous
            )
            return window, "AI_PATTERN_ANALYSIS"
        except Exception:
            # Safe fail-closed exception fallback
            fallback_score = 0.95 if len(entries) >= 3 else 0.0
            window = SequenceTrajectoryWindow(
                start_time=entries[0].timestamp if entries else time.time(),
                end_time=entries[-1].timestamp if entries else time.time(),
                entries=entries,
                ordered_pattern_score=fallback_score,
                is_anomalous=(fallback_score >= self.anomaly_threshold)
            )
            return window, "EXCEPTION_FALLBACK_TRIGGER"
