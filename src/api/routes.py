import random
import time
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Request
from src.models.telemetry import RawTelemetryInput, AuthenticationEntryDigest
from src.services.anonymizer import TelemetryAnonymizer
from src.services.anomaly_detector import AIAnomalyDetector
from src.services.lockup_service import SecurityLockupService
from src.services.audit_logger import AuditLogger

router = APIRouter(prefix="/api/v1")

anonymizer = TelemetryAnonymizer()
detector = AIAnomalyDetector()
audit_logger = AuditLogger()
lockup_service = SecurityLockupService(audit_logger=audit_logger)

sliding_window_buffer: List[AuthenticationEntryDigest] = []
total_ingested_count: int = 0
total_blocked_count: int = 0
total_anomalies_detected: int = 0


@router.api_route("/telemetry/ingest", methods=["GET", "POST"])
async def ingest_telemetry(raw_input: RawTelemetryInput = None, request: Request = None) -> Dict[str, Any]:
    global sliding_window_buffer, total_ingested_count, total_blocked_count, total_anomalies_detected
    
    if raw_input is None and request is not None:
        try:
            body = await request.json()
            raw_input = RawTelemetryInput(**body)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid payload")
            
    if raw_input is None:
        raise HTTPException(status_code=400, detail="Missing telemetry payload")

    total_ingested_count += 1
    digest = anonymizer.anonymize(raw_input)

    # Check if account or IP is already locked out
    if lockup_service.is_account_locked(digest.account_digest):
        total_blocked_count += 1
        return {
            "status": "BLOCKED",
            "message": "Account is locked due to active security lockout.",
            "lockup_activated": True
        }
    if lockup_service.is_ip_isolated(digest.ip_hash):
        total_blocked_count += 1
        return {
            "status": "BLOCKED",
            "message": "Source IP vector is isolated.",
            "lockup_activated": True
        }

    # Add digest and purge entries older than 60 seconds from sliding trajectory window
    sliding_window_buffer.append(digest)
    cutoff_time = digest.timestamp - 60.0
    sliding_window_buffer = [e for e in sliding_window_buffer if e.timestamp >= cutoff_time]

    if len(sliding_window_buffer) > 100:
        sliding_window_buffer = sliding_window_buffer[-100:]

    # Evaluate trajectory window
    window_res, trigger_type = detector.evaluate_window(sliding_window_buffer)

    if window_res.is_anomalous:
        total_anomalies_detected += 1
        # Trigger automated lockup
        target_accounts = list(set(e.account_digest for e in sliding_window_buffer))
        source_ips = list(set(e.ip_hash for e in sliding_window_buffer))

        event = lockup_service.trigger_lockup(
            reason=f"ORDERED_BREACH_DETECTED_{trigger_type}",
            confidence_score=window_res.ordered_pattern_score,
            account_digests=target_accounts,
            ip_hashes=source_ips
        )

        return {
            "status": "SECURITY_LOCKUP_ACTIVATED",
            "anomaly_score": round(window_res.ordered_pattern_score, 4),
            "lockup_activated": True,
            "lockup_id": event.lockup_id,
            "trigger_reason": event.trigger_reason
        }

    return {
        "status": "PROCESSED",
        "anomaly_score": round(window_res.ordered_pattern_score, 4),
        "lockup_activated": False,
        "lockup_id": None
    }


@router.get("/incidents")
def get_incident_audit_trail() -> List[Dict[str, Any]]:
    return audit_logger.get_recent_events()


@router.get("/lockups/active")
def get_active_lockups() -> List[Dict[str, Any]]:
    active_events = lockup_service.get_active_lockups()
    return [e.model_dump() for e in active_events]


@router.get("/stats")
def get_system_stats() -> Dict[str, Any]:
    active_lockups = lockup_service.get_active_lockups()
    return {
        "total_ingested": total_ingested_count,
        "total_blocked": total_blocked_count,
        "total_anomalies": total_anomalies_detected,
        "active_lockouts": len(active_lockups),
        "isolated_ips": len(lockup_service.isolated_ips),
        "locked_accounts": len(lockup_service.locked_accounts),
        "buffer_size": len(sliding_window_buffer)
    }


@router.api_route("/lockup/resolve/{lockup_id}", methods=["GET", "POST"])
def resolve_lockup(lockup_id: str) -> Dict[str, Any]:
    success = lockup_service.resolve_lockup(lockup_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lockup ID not found or already resolved.")
    return {"status": "RESOLVED", "lockup_id": lockup_id}


@router.api_route("/simulation/attack", methods=["GET", "POST"])
async def run_attack_simulation() -> Dict[str, Any]:
    random_octet = random.randint(10, 250)
    attack_ip = f"198.51.100.{random_octet}"
    target_accounts = [f"bot_target_{random_octet}_{i}" for i in range(1, 6)]
    base_time = time.time()
    results = []

    for idx, account in enumerate(target_accounts):
        inp = RawTelemetryInput(
            account_identifier=account,
            ip_address=attack_ip,
            char_length=8 + idx,
            timestamp=base_time + (idx * 0.05)
        )
        res = await ingest_telemetry(raw_input=inp)
        res["target_account"] = account
        res["attempt_number"] = idx + 1
        results.append(res)

    return {
        "simulation_type": "AUTOMATED_CREDENTIAL_STUFFING",
        "simulated_ip": attack_ip,
        "results": results
    }


@router.api_route("/simulation/legit", methods=["GET", "POST"])
async def run_legit_user_simulation() -> Dict[str, Any]:
    random_octet = random.randint(10, 250)
    user_ip = f"198.51.100.{random_octet}"
    single_account = f"john_doe_{random_octet}"
    base_time = time.time()
    human_delays = [0.0, 2.5, 6.6, 9.6, 14.8]
    results = []

    for idx, delay in enumerate(human_delays):
        inp = RawTelemetryInput(
            account_identifier=single_account,
            ip_address=user_ip,
            char_length=8 + (idx % 3),
            timestamp=base_time + delay
        )
        res = await ingest_telemetry(raw_input=inp)
        res["target_account"] = single_account
        res["attempt_number"] = idx + 1
        results.append(res)

    return {
        "simulation_type": "LEGITIMATE_USER_RETRY",
        "simulated_ip": user_ip,
        "results": results
    }
