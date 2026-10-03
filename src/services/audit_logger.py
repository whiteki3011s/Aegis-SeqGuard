import os
import json
import time
from typing import Dict, Any, List
from src.models.lockup import SecurityLockupEvent


class AuditLogger:
    def __init__(self, log_path: str = "audit_events.jsonl"):
        self.log_path = log_path

    def log_lockup_event(self, event: SecurityLockupEvent) -> str:
        record = {
            "event_type": "SECURITY_LOCKUP",
            "lockup_id": event.lockup_id,
            "triggered_at": event.triggered_at,
            "formatted_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(event.triggered_at)),
            "trigger_reason": event.trigger_reason,
            "confidence_score": event.confidence_score,
            "locked_account_digests": event.locked_account_digests,
            "isolated_ip_hashes": event.isolated_ip_hashes,
            "status": event.status.value
        }
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            
        return event.lockup_id

    def get_recent_events(self, max_records: int = 50) -> List[Dict[str, Any]]:
        if not os.path.exists(self.log_path):
            return []
            
        events = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events[-max_records:]
