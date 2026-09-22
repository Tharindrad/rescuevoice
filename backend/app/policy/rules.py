ACTION_RULES={
 "upload_corrected_passport":{"risk":"medium","requires_consent":True},
 "book_appointment":{"risk":"medium","requires_consent":True},
}
FORBIDDEN={"approve_application","reject_application","change_final_decision","delete_application","change_identity","bypass_verification"}

def evaluate(action, case, *, verified, consent):
    if not verified: return {"allowed":False,"reason":"Approved verification must pass before consequential actions.","code":"VERIFICATION_REQUIRED","retryable":False,"human_required":False}
    if action in FORBIDDEN: return {"allowed":False,"reason":"Final or privileged decisions cannot be delegated to the voice agent.","code":"POLICY_DENIED","retryable":False,"human_required":True}
    rule=ACTION_RULES.get(action)
    if not rule: return {"allowed":False,"reason":"Action is outside the agent's approved tool policy.","code":"ACTION_NOT_ALLOWLISTED","retryable":False,"human_required":True}
    if rule["requires_consent"] and not consent: return {"allowed":False,"reason":"Explicit caller consent is required before this action.","code":"CONSENT_REQUIRED","retryable":False,"human_required":False}
    if action not in case.get("allowed_actions",[]): return {"allowed":False,"reason":"This action is not approved for the current application.","code":"CASE_ACTION_DENIED","retryable":False,"human_required":True}
    return {"allowed":True,"reason":"Approved by policy.","code":"POLICY_ALLOWED","retryable":False,"human_required":False}
