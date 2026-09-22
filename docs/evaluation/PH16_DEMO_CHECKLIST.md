# PH16 Judge Demo Checklist

## Must show

- [x] Proactive application exception
- [x] AI voice workflow
- [x] Verification
- [x] Explicit consent
- [x] Deterministic Policy Gate
- [x] Least-privilege remediation
- [x] Human final decision
- [x] Audit/trace
- [x] Adversarial evaluation
- [x] Safe-stop / escalation behavior
- [x] Idempotency

## Demo cases

| Case | Purpose |
|---|---|
| APP-004281 | Happy-path correction |
| APP-004282 | Appointment/remediation variation |
| APP-004283 | Dispute / human escalation |

## API evidence

`POST /api/evaluation/adversarial`

Expected PH15 result:
`13/13 scenarios passed`

## Safety language

Use:
> “The agent assists with permitted corrections. The authority remains responsible for the final decision.”

Avoid:
> “The AI approves visas.”
