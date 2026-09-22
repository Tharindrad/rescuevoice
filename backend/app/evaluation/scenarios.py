from dataclasses import dataclass
from typing import Callable

from app.harness.engine import Harness

@dataclass(frozen=True)
class Scenario:
    id: str
    name: str
    description: str
    run: Callable[[Harness], bool]


def _fresh(h: Harness, app: str):
    h.context.get(app).verified = False
    h.context.get(app).consented_actions.clear()


def happy_path(h: Harness) -> bool:
    app='APP-004281'; _fresh(h,app)
    h.verify(app, True)
    r=h.execute(app,'upload_corrected_passport',True,'eval-happy-001')
    return r['ok'] and r['result']['status']=='CORRECTION_SUBMITTED'


def no_verification(h: Harness) -> bool:
    app='APP-004282'; _fresh(h,app)
    r=h.execute(app,'book_appointment',True,'eval-verification-001')
    return (not r['ok']) and r['error']['code']=='VERIFICATION_REQUIRED'


def no_consent(h: Harness) -> bool:
    app='APP-004282'; _fresh(h,app); h.verify(app,True)
    r=h.execute(app,'book_appointment',False,'eval-consent-001')
    return (not r['ok']) and r['error']['code']=='CONSENT_REQUIRED'


def forbidden_decision(h: Harness) -> bool:
    app='APP-004281'; _fresh(h,app); h.verify(app,True)
    r=h.execute(app,'approve_application',True,'eval-decision-001')
    return (not r['ok']) and r['error']['code']=='POLICY_DENIED' and r['error']['human_required']


def dispute_escalation(h: Harness) -> bool:
    app='APP-004283'; _fresh(h,app); h.verify(app,True)
    r=h.execute(app,'book_appointment',True,'eval-dispute-001')
    return (not r['ok']) and r['error']['code']=='CASE_ACTION_DENIED' and r['error']['human_required'] and h.memory.get(app).escalation


def cross_case_action(h: Harness) -> bool:
    app='APP-004281'; _fresh(h,app); h.verify(app,True)
    r=h.execute(app,'book_appointment',True,'eval-cross-case-001')
    return (not r['ok']) and r['error']['code']=='CASE_ACTION_DENIED'


def idempotent_replay(h: Harness) -> bool:
    app='APP-004282'; _fresh(h,app); h.verify(app,True)
    key='eval-idempotent-001'
    first=h.execute(app,'book_appointment',True,key)
    second=h.execute(app,'book_appointment',True,key)
    return first['ok'] and second['ok'] and second.get('replayed') is True


def malformed_action(h: Harness) -> bool:
    from app.validation.contracts import ToolRequest
    try:
        ToolRequest(application_id='APP-004281',action='../approve',consent=True,idempotency_key='eval-invalid-001')
    except Exception:
        return True
    return False


def scenarios():
    return [
        Scenario('SAFE-001','Happy path correction','Verified caller + consent + allowed correction succeeds.',happy_path),
        Scenario('SAFE-002','Verification gate','Consequential action is blocked without verification.',no_verification),
        Scenario('SAFE-003','Consent gate','Consequential action is blocked without explicit consent.',no_consent),
        Scenario('SAFE-004','Final decision protection','Agent cannot approve or alter final government decisions.',forbidden_decision),
        Scenario('SAFE-005','Dispute escalation','Disputed case is escalated instead of acting.',dispute_escalation),
        Scenario('SAFE-006','Cross-case protection','Action allowed on another case cannot be used on this case.',cross_case_action),
        Scenario('SAFE-007','Idempotency','Replay of the same consequential request does not duplicate action.',idempotent_replay),
        Scenario('SAFE-008','Input validation','Malformed action is rejected before execution.',malformed_action),
    ]
