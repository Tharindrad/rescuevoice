from dataclasses import dataclass
from typing import Any

@dataclass
class AgentError:
    code: str
    message: str
    retryable: bool
    human_required: bool = False
    details: dict[str, Any] | None = None
    def as_dict(self): return {"code":self.code,"message":self.message,"retryable":self.retryable,"human_required":self.human_required,"details":self.details or {}}
