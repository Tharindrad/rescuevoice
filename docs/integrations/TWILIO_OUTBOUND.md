# PH13 — Twilio Outbound Calls

RescueVoice uses ElevenLabs' native Twilio outbound-call integration.

## Current flow

React dashboard → RescueVoice FastAPI → ElevenLabs outbound-call API → Twilio → applicant phone → ElevenLabs Agent.

The browser never receives Twilio or ElevenLabs credentials.

## Required configuration

```env
ELEVENLABS_API_KEY=...
ELEVENLABS_AGENT_ID=...
ELEVENLABS_AGENT_PHONE_NUMBER_ID=...
ELEVENLABS_WEBHOOK_SECRET=...
```

The ElevenLabs agent phone number must be connected to the Twilio setup. The destination number must be E.164 formatted, e.g. `+9715XXXXXXXX`.

## UI

Open an application and use the **Twilio outbound · test only** field. Enter an authorized test number and press **Call applicant**.

## Safety

- Outbound calls are disabled until provider configuration exists.
- E.164 validation is server-side.
- Only application records known to the Government mock are callable.
- Recording is explicitly configurable.
- Real production use requires lawful consent, call-recording notices, retention controls, and jurisdiction-specific telecom/privacy review.
- Never put credentials in React or commit `.env`.

## Alternative advanced integration

ElevenLabs also supports a register-call pattern where developers own Twilio infrastructure and return ElevenLabs-generated TwiML to Twilio. We are using the native integration for this milestone because it is simpler for the competition demo.
