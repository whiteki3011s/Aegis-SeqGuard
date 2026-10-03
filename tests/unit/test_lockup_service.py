import os
from src.services.lockup_service import SecurityLockupService
from src.services.audit_logger import AuditLogger
from src.models.lockup import LockupStatus


def test_lockup_trigger_and_resolve(tmp_path):
    audit_file = str(tmp_path / "test_audit.jsonl")
    audit_logger = AuditLogger(log_path=audit_file)
    service = SecurityLockupService(audit_logger=audit_logger)

    account_hash = "abc123hash"
    ip_hash = "ip456hash"

    # Trigger lockup
    event = service.trigger_lockup(
        reason="TEST_DICTIONARY_ATTACK",
        confidence_score=0.92,
        account_digests=[account_hash],
        ip_hashes=[ip_hash]
    )

    assert event.status == LockupStatus.ACTIVE
    assert service.is_account_locked(account_hash)
    assert service.is_ip_isolated(ip_hash)

    # Verify audit file logged
    events = audit_logger.get_recent_events()
    assert len(events) == 1
    assert events[0]["lockup_id"] == event.lockup_id

    # Resolve lockup
    resolved = service.resolve_lockup(event.lockup_id)
    assert resolved
    assert not service.is_account_locked(account_hash)
    assert not service.is_ip_isolated(ip_hash)
