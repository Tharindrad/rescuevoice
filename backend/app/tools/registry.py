from dataclasses import dataclass
from typing import Callable
from app.tools.government import get_application, get_issue, execute

@dataclass(frozen=True)
class ToolSpec:
    name: str
    risk: str
    handler: Callable
    consequential: bool

TOOLS={
 'get_application':ToolSpec('get_application','low',get_application,False),
 'get_application_issue':ToolSpec('get_application_issue','low',get_issue,False),
 'submit_correction':ToolSpec('submit_correction','medium',lambda application_id,idempotency_key: execute('upload_corrected_passport',application_id,idempotency_key),True),
 'book_appointment':ToolSpec('book_appointment','medium',lambda application_id,idempotency_key: execute('book_appointment',application_id,idempotency_key),True),
}
FORBIDDEN_TOOLS={'approve_application','reject_application','delete_application','change_final_decision','bypass_verification'}

def resolve(name:str):
    if name in FORBIDDEN_TOOLS: raise PermissionError('Tool is permanently unavailable to the agent.')
    return TOOLS.get(name)
