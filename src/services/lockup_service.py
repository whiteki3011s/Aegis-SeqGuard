import time
from typing import Dict, Set, Optional, List
from src.models.lockup import SecurityLockupEvent, LockupStatus
from src.services.audit_logger import AuditLogger


class SecurityLockupService:
    def __init__(self, audit_logger: Optional[AuditLogger] = None):
        self.locked_accounts: Set[str] = set()
        self.isolated_ips: Set[str] = set()
        self.active_events: Dict[str, SecurityLockupEvent] = {}
        self.audit_logger = audit_logger or AuditLogger()

    def trigger_lockup(
        self,
        reason: str,
        confidence_score: float,
        account_digests: List[str],
        ip_hashes: List[str]
    ) -> SecurityLockupEvent:
        event = SecurityLockupEvent(
            triggered_at=time.time(),
            trigger_reason=reason,
            confidence_score=confidence_score,
            locked_account_digests=account_digests,
            isolated_ip_hashes=ip_hashes,
            status=LockupStatus.ACTIVE
        )

        for acct in account_digests:
            self.locked_accounts.add(acct)
        for ip in ip_hashes:
            self.isolated_ips.add(ip)

        self.active_events[event.lockup_id] = event
        self.audit_logger.log_lockup_event(event)

        return event

    def is_account_locked(self, account_digest: str) -> bool:
        return account_digest in self.locked_accounts

    def is_ip_isolated(self, ip_hash: str) -> bool:
        return ip_hash in self.isolated_ips

    def resolve_lockup(self, lockup_id: str) -> bool:
        if lockup_id not in self.active_events:
            return False

        event = self.active_events[lockup_id]
        event.status = LockupStatus.RESOLVED

        for acct in event.locked_account_digests:
            self.locked_accounts.discard(acct)
        for ip in event.isolated_ip_hashes:
            self.isolated_ips.discard(ip)

        self.audit_logger.log_lockup_event(event)
        return True

    def get_active_lockups(self) -> List[SecurityLockupEvent]:
        return [e for e in self.active_events.values() if e.status == LockupStatus.ACTIVE]


