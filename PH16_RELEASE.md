# RescueVoice PH16 — Final Demo Release

## Demo objective

Show the judging panel one complete, understandable story:

**Exception → Voice outreach → Verification → Explanation → Consent → Policy Gate → Safe remediation → Audit → Human final decision**

## 90-second demo script

### 0–10s — Problem
Open Overview and select `APP-004281`.

Say:
> “A resident's application has a correctable issue. Instead of discovering it later, RescueVoice proactively reaches out.”

### 10–25s — Voice
Open **Live voice** or show the ElevenLabs-connected call when credentials are configured.

Say:
> “The agent identifies itself as AI, uses the applicant's preferred language, and explains only the recorded application issue.”

### 25–40s — Verification + consent
Show the workflow advancing through:
- Identify
- Verify
- Explain
- Consent

Say:
> “Verification and explicit consent happen before any consequential action.”

### 40–55s — Policy Gate
Show **Policy Gate** / backend evaluation.

Say:
> “The model cannot grant itself permission. The server-side Policy Gate decides whether the exact action is allow-listed for this case.”

### 55–70s — Remediation
Execute `upload_corrected_passport`.

Show:
- correction submitted
- audit event
- final decision owner = government officer

Say:
> “RescueVoice performs only the permitted correction. It does not approve the application.”

### 70–85s — Attack
Use `APP-004283` or the PH15 evaluation endpoint.

Run:
`POST /api/evaluation/adversarial`

Highlight:
- prompt injection → BLOCKED
- approve/bypass → BLOCKED + HUMAN
- no consent → BLOCKED
- dispute → ESCALATE
- duplicate retry → IDEMPOTENT

### 85–90s — Closing
Say:
> “The differentiator is not that the AI can complete a workflow. It is that the AI is structurally prevented from completing workflows it is not authorized to perform.”

## Recording checklist

- [ ] Browser zoom 90–100%
- [ ] Hide devtools
- [ ] Use sandbox/mock application IDs
- [ ] Show AI disclosure
- [ ] Keep Policy Gate visible during action
- [ ] Show human final decision ownership
- [ ] Show at least one adversarial test
- [ ] Never expose API keys, webhook secrets, phone numbers, or private applicant data
- [ ] If live telephony is unstable, use the deterministic simulation and clearly label it as simulation

## Evidence to capture

1. Overview dashboard
2. APP-004281 case drawer
3. Live voice / simulated workflow
4. Policy Gate result
5. Successful remediation + audit
6. PH15 adversarial results
7. APP-004283 human escalation
8. Architecture diagram / README

## Release claim

PH15 adversarial suite: **13 scenarios, 100% pass**.

The wider regression suite from the PH15 development pass still contained pre-existing integration mismatches; therefore this release does **not** claim that every historical test is green.
