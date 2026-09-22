# PH14 — Full End-to-End Test Plan

## Objective

Prove that the RescueVoice control plane works from an application exception through verification, consent, policy authorization, approved government action, audit, and human final decision.

## Primary path

1. Application exception loaded.
2. Voice/session context identifies the application.
3. Applicant verification succeeds.
4. Rejection/correction issue is retrieved.
5. Explicit consent is obtained.
6. Harness Policy Gate validates the exact allow-listed action.
7. Government action executes once with idempotency protection.
8. Application moves to human review.
9. Audit/trace data is retained.
10. Human officer remains the final decision owner.

## Negative paths

- Verification failure → no state-changing action.
- No consent → policy block.
- Forbidden action → hard block + escalation.
- Disputed decision → human escalation.
- Unknown application → 404 / safe stop.
- Duplicate request → idempotent replay.
- Provider unavailable → no government action.
- Invalid phone number → outbound call rejected before provider call.

## Provider boundary

PH14 deliberately separates provider availability from control-plane correctness. ElevenLabs/Twilio calls are tested through their adapters only when credentials exist. The deterministic E2E suite proves the Harness path without requiring paid or external services.

## Release criteria

- All backend tests pass.
- Primary correction path passes.
- At least one escalation path passes.
- Idempotency replay passes.
- No forbidden action reaches the government tool.
- Final decision owner remains the authority officer.
