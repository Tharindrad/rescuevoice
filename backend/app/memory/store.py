from dataclasses import dataclass, field
from typing import Any

@dataclass
class CaseMemory:
    application_id: str
    completed_actions: list[str] = field(default_factory=list)
    failed_actions: list[str] = field(default_factory=list)
    escalation: bool = False
    consent_events: list[str] = field(default_factory=list)
    audit_events: list[dict[str,Any]] = field(default_factory=list)

class MemoryStore:
    def __init__(self): self._cases: dict[str,CaseMemory]={}
    def get(self, application_id): return self._cases.setdefault(application_id,CaseMemory(application_id))
    def record_consent(self, application_id, action): self.get(application_id).consent_events.append(action)
    def snapshot(self, application_id):
        c=self.get(application_id); return {"application_id":c.application_id,"completed_actions":c.completed_actions.copy(),"failed_actions":c.failed_actions.copy(),"escalation":c.escalation,"consent_events":c.consent_events.copy(),"audit_events":c.audit_events.copy()}
