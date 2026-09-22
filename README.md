# RescueVoice

**Governance-first AI voice agent for resolving correctable government application exceptions.**

RescueVoice proactively contacts applicants when a submitted government application contains a correctable issue. It explains the issue in the applicant's preferred language, verifies identity through an approved challenge, obtains explicit consent, and then either performs an authorized correction or books an appointment. Final application decisions always remain with the government authority.

> **Track:** Government Services — Proactive Application Resolution  
> **Challenge:** Future of Voice AI Challenge — ElevenLabs × Ignyte  
> **Stage 1 Proof of Build:** This public repository

## Why RescueVoice

Government applications are often delayed by small, correctable errors. RescueVoice is designed as an exception-resolution layer between an authority's application system and the resident, reducing avoidable call-center contacts and repeat visits while keeping high-impact decisions under human authority.

## Core Flow

```text
Government Application System
        ↓
Correctable exception detected
        ↓
ElevenLabs Voice Agent
        ↓
Identity verification
        ↓
Explain issue in preferred language
        ↓
Explicit consent
        ↓
Policy Gate / Harness
   ├─ Authorized → correction or appointment tool
   ├─ Blocked → safe explanation
   └─ Dispute / uncertainty / vulnerability → human escalation
        ↓
Audit trail + transcript
        ↓
Government officer retains final decision
```

## Architecture

RescueVoice separates conversational intelligence from execution authority:

- **ElevenLabs** — voice and conversational interface.
- **FastAPI backend** — API boundary and orchestration.
- **Harness / Policy Gate** — deterministic permission, verification, consent, risk, retry, and stop controls.
- **Loop Engine** — `Act → Observe → Judge → Adjust → Stop` with bounded retries.
- **Approved Tools** — allow-listed government actions only.
- **Audit / Observability** — trace IDs, structured events, case-scoped memory.
- **Human authority** — final approval/rejection decisions remain outside the AI agent.

## Safety Model

The language model cannot grant itself permissions. Consequential actions are enforced server-side.

Key controls:

- approved verification required before protected actions;
- explicit consent before consequential actions;
- least-privilege tool allow-list;
- forbidden actions such as approving/rejecting an application or bypassing verification;
- idempotency protection for duplicate actions;
- bounded retries and safe-stop behaviour;
- disputes, distress, policy ambiguity, or unsupported exceptions escalate to a human;
- audit events and trace IDs for consequential actions.

See [`docs/AGENT_ETHICS_AND_CONDUCT.md`](docs/AGENT_ETHICS_AND_CONDUCT.md).

## Demo Cases

The mock government service includes scenarios such as:

- correctable residency-document issue → authorized correction;
- licence renewal requiring in-person attendance → appointment booking;
- applicant dispute → no automated correction and human escalation.

## Current Build Status

- FastAPI backend implemented.
- React + Vite + TypeScript dashboard implemented.
- ElevenLabs signed-session integration boundary implemented.
- ElevenLabs native Twilio outbound-call adapter implemented.
- Policy Gate / Harness implemented.
- Case-scoped memory, structured errors, observability, and idempotency implemented.
- Adversarial evaluation suite implemented.
- Backend automated test suite: **34/34 passing** in the current release candidate.
- PH15 adversarial scenarios: **13/13 passing**.

The frontend source and configuration are included. A production frontend build should be verified locally after installing Node dependencies.

## Repository Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── context/
│   │   ├── errors/
│   │   ├── evaluation/
│   │   ├── harness/
│   │   ├── integrations/
│   │   ├── loop/
│   │   ├── memory/
│   │   ├── observability/
│   │   ├── policy/
│   │   ├── tools/
│   │   └── validation/
│   └── tests/
├── docs/
│   ├── evaluation/
│   └── integrations/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
├── .env.example
├── docker-compose.yml
├── package.json
├── run_demo.sh
└── start.py
```

## Run the Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs will be available at:

```text
http://localhost:8000/docs
```

## Run Backend Tests

```bash
cd backend
pytest -q
```

## Run the Frontend

```bash
npm install
npm run dev
```

By default the frontend expects the API at `http://localhost:8000/api`. Override it with `VITE_API_BASE_URL` if required.

## Environment Variables

Copy the example file:

```bash
cp .env.example .env
```

Required only for real voice/telephony integration:

```text
ELEVENLABS_API_KEY=
ELEVENLABS_AGENT_ID=
ELEVENLABS_AGENT_PHONE_NUMBER_ID=
TWILIO_PHONE_NUMBER=
```

**Never commit real API keys or secrets.**

## Important API Endpoints

```text
POST /api/verify
GET  /api/applications/{application_id}
POST /api/policy/check
POST /api/actions/execute
POST /api/loop/run
GET  /api/memory/{application_id}
GET  /api/elevenlabs/signed-url
POST /api/outbound-call
POST /api/evaluation/adversarial
```

## ElevenLabs Integration

The browser never receives the ElevenLabs API key. The backend generates the signed conversation URL and keeps provider credentials server-side. Outbound telephony uses the server-side ElevenLabs/Twilio integration adapter.

See:

- [`docs/integrations/ELEVENLABS_REAL_INTEGRATION.md`](docs/integrations/ELEVENLABS_REAL_INTEGRATION.md)
- [`docs/integrations/TWILIO_OUTBOUND.md`](docs/integrations/TWILIO_OUTBOUND.md)
- [`docs/integrations/ELEVENLABS_AGENT_CONTRACT.md`](docs/integrations/ELEVENLABS_AGENT_CONTRACT.md)

## Evaluation

The project includes deterministic evaluation of failure and adversarial scenarios including:

- wrong identity / repeated verification failure;
- requests for unpermitted approval actions;
- legal dispute;
- prompt injection attempts;
- missing consent;
- government API timeout;
- voice/telephony failure;
- duplicate action retry;
- distress signals;
- unsupported rejection types;
- language switching.

See [`docs/evaluation/PH15_EVALUATION_REPORT.md`](docs/evaluation/PH15_EVALUATION_REPORT.md).

## Scope Boundary

RescueVoice is designed to resolve **correctable issues in already-submitted applications**. It does not create new applications, make final eligibility determinations, approve or reject applications, or bypass official verification and policy controls.

## License / Prototype Notice

Hackathon prototype. Government integrations in this repository are mocked unless explicitly configured against an authorized external service. Do not use production personal data or production government credentials in the demo environment.
