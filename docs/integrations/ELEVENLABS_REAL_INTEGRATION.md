# RescueVoice PH12 — ElevenLabs Real Integration

## Architecture

React → `/api/elevenlabs/signed-url` → ElevenLabs Agent → webhook tools → RescueVoice Harness → Government APIs.

The ElevenLabs API key never reaches the browser. The FastAPI server requests a temporary signed URL and the React SDK starts the session with that URL.

## Frontend

Install:

```bash
npm install @elevenlabs/react
```

The app uses `ConversationProvider` and `useConversationControls`.

## Backend environment

```env
ELEVENLABS_API_KEY=your_key
ELEVENLABS_AGENT_ID=agent_xxx
ELEVENLABS_WEBHOOK_SECRET=your_webhook_secret
```

## Agent tools

Configure these as ElevenLabs Webhook tools:

- `get_application`
- `get_application_issue`
- `submit_correction`
- `book_appointment`

For state-changing tools, the webhook endpoint must call the RescueVoice Harness. The LLM must not bypass verification, consent, policy checks, idempotency, or audit logging.

## Agent system prompt constraints

1. Identify as an AI assistant.
2. Use the application context supplied by the server.
3. Verify before discussing or changing protected application data.
4. Explain only the issue returned by the government API.
5. Obtain explicit consent immediately before a state-changing action.
6. Never approve, reject, alter final decisions, change identity, or bypass verification.
7. If the caller disputes the decision, policy is uncertain, verification fails, or the caller needs human assistance, stop and escalate.
8. Never request passwords, PINs, OTPs, or other secrets.
9. Preserve the caller's preferred language; English and Arabic are the initial supported languages.

## Current provider boundary

The React SDK is the voice transport and conversation interface. RescueVoice remains the control plane. Government actions are executed only through the Harness.
