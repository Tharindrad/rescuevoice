import os
from typing import Any

import httpx

from app.integrations.elevenlabs.client import ElevenLabsAPIError, ElevenLabsConfigurationError


class ElevenLabsOutboundClient:
    """Provider adapter for ElevenLabs-managed outbound calls.

    The browser never receives provider credentials. The Harness remains the
    authority for application actions; this client only starts a voice call.
    """

    def __init__(self, timeout: float = 20.0):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.agent_id = os.getenv("ELEVENLABS_AGENT_ID")
        self.agent_phone_number_id = os.getenv("ELEVENLABS_AGENT_PHONE_NUMBER_ID")
        self.base_url = os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io").rstrip("/")
        self.timeout = timeout

    def validate(self) -> None:
        missing = [
            name for name, value in {
                "ELEVENLABS_API_KEY": self.api_key,
                "ELEVENLABS_AGENT_ID": self.agent_id,
                "ELEVENLABS_AGENT_PHONE_NUMBER_ID": self.agent_phone_number_id,
            }.items() if not value
        ]
        if missing:
            raise ElevenLabsConfigurationError("Missing outbound configuration: " + ", ".join(missing))

    def start_call(self, to_number: str, *, application_id: str) -> dict[str, Any]:
        self.validate()
        payload = {
            "agent_id": self.agent_id,
            "agent_phone_number_id": self.agent_phone_number_id,
            "to_number": to_number,
            "conversation_initiation_client_data": {
                "dynamic_variables": {"application_id": application_id}
            },
            "call_recording_enabled": True,
        }
        try:
            response = httpx.post(
                f"{self.base_url}/v1/convai/twilio/outbound-call",
                headers={"xi-api-key": self.api_key or "", "Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout,
            )
        except httpx.HTTPError as exc:
            raise ElevenLabsAPIError(f"Outbound call request failed: {exc}") from exc
        if response.is_error:
            raise ElevenLabsAPIError(
                f"ElevenLabs outbound call returned HTTP {response.status_code}: {response.text[:300]}"
            )
        body = response.json()
        if not body.get("success"):
            raise ElevenLabsAPIError("ElevenLabs outbound call was not accepted")
        return body
