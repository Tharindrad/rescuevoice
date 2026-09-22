from typing import Any
GOVERNMENT={
 "APP-004281":{"id":"APP-004281","applicant":"Ahmed","language":"Arabic","service":"Residency renewal","status":"CORRECTION_REQUIRED","issue":"Expired passport document","allowed_actions":["upload_corrected_passport"],"final_decision_owner":"government_officer"},
 "APP-004282":{"id":"APP-004282","applicant":"Maria","language":"English","service":"Licence renewal","status":"APPOINTMENT_REQUIRED","issue":"In-person attendance required","allowed_actions":["book_appointment"],"final_decision_owner":"government_officer"},
 "APP-004283":{"id":"APP-004283","applicant":"Omar","language":"Arabic","service":"Permit","status":"DISPUTE","issue":"Applicant disputes the decision","allowed_actions":[],"final_decision_owner":"government_officer"},
}

def get_application(application_id): return GOVERNMENT.get(application_id)
def get_issue(application_id):
    c=get_application(application_id); return {"issue":c["issue"],"status":c["status"]} if c else None

def execute(action, application_id, idempotency_key):
    c=GOVERNMENT.get(application_id)
    if not c: return {"ok":False,"error":{"code":"NOT_FOUND","message":"Application not found","retryable":False,"human_required":False}}
    if action not in c["allowed_actions"]: return {"ok":False,"error":{"code":"TOOL_POLICY_MISMATCH","message":"Action is not permitted for this case","retryable":False,"human_required":True}}
    if action=="upload_corrected_passport": c["status"]="CORRECTION_SUBMITTED"
    elif action=="book_appointment": c["status"]="APPOINTMENT_BOOKED"
    return {"ok":True,"status":c["status"],"final_decision_owner":c["final_decision_owner"],"idempotency_key":idempotency_key}
