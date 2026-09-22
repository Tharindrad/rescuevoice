import os
import re
from dataclasses import dataclass
from typing import Any

import httpx


class ElevenLabsConfigurationError(RuntimeError):
    pass


class ElevenLabsAPIError(RuntimeError):
    pass


@dataclass(frozen=True)
class ElevenLabsConfig:
    api_key: str | None
    agent_id: str | None
    environment: str = "production"
    base_url: str = "https://api.elevenlabs.io"

    @classmethod
    def from_env(cls) -> "ElevenLabsConfig":
        return cls(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            agent_id=os.getenv("ELEVENLABS_AGENT_ID"),
            environment=os.getenv("ELEVENLABS_ENVIRONMENT", "production"),
            base_url=os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io").rstrip("/"),
        )

    def validate_for_signed_url(self) -> None:
        if not self.api_key:
            raise ElevenLabsConfigurationError("ELEVENLABS_API_KEY is not configured")
        if not self.agent_id:
            raise ElevenLabsConfigurationError("ELEVENLABS_AGENT_ID is not configured")


class ElevenLabsClient:
    """Small provider adapter; the Harness remains the action authority."""

    def __init__(self, config: ElevenLabsConfig | None = None, timeout: float = 15.0):
        self.config = config or ElevenLabsConfig.from_env()
        self.timeout = timeout

    def get_signed_url(self, *, include_conversation_id: bool = False) -> dict[str, Any]:
        self.config.validate_for_signed_url()
        params = {
            "agent_id": self.config.agent_id,
            "include_conversation_id": str(include_conversation_id).lower(),
            "environment": self.config.environment,
        }
        headers = {"xi-api-key": self.config.api_key or ""}
        try:
            response = httpx.get(
                f"{self.config.base_url}/v1/convai/conversation/get-signed-url",
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
        except httpx.HTTPError as exc:
            raise ElevenLabsAPIError(f"ElevenLabs request failed: {exc}") from exc
        if response.is_error:
            raise ElevenLabsAPIError(
                f"ElevenLabs returned HTTP {response.status_code}: {response.text[:300]}"
            )
        body = response.json()
        if not body.get("signed_url"):
            raise ElevenLabsAPIError("ElevenLabs response did not contain signed_url")
        return body


    def outbound_call(
        self,
        *,
        agent_id: str,
        agent_phone_number_id: str,
        to_number: str,
        application_id: str,
        applicant_name: str,
        language: str,
        call_recording_enabled: bool = True,
    ) -> dict:
        """Start an outbound call through ElevenLabs' native Twilio integration."""
        if not re.fullmatch(r"\+[1-9]\d{7,14}", to_number):
            raise ValueError("Phone number must use E.164 format.")
        payload = {
            "agent_id": agent_id,
            "agent_phone_number_id": agent_phone_number_id,
            "to_number": to_number,
            "call_recording_enabled": call_recording_enabled,
            "conversation_initiation_client_data": {
                "dynamic_variables": {
                    "application_id": application_id,
                    "applicant_name": applicant_name,
                    "preferred_language": language,
                }
            },
        }
        return self._request("POST", "/v1/convai/twilio/outbound-call", json=payload)


    def _request(self, method: str, path: str, *, json: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.config.api_key:
            raise ElevenLabsConfigurationError("ELEVENLABS_API_KEY is not configured")
        headers = {"xi-api-key": self.config.api_key, "Content-Type": "application/json"}
        try:
            response = httpx.request(
                method,
                f"{self.config.base_url}{path}",
                headers=headers,
                json=json,
                timeout=self.timeout,
            )
        except httpx.HTTPError as exc:
            raise ElevenLabsAPIError(f"ElevenLabs request failed: {exc}") from exc
        if response.is_error:
            raise ElevenLabsAPIError(
                f"ElevenLabs returned HTTP {response.status_code}: {response.text[:300]}"
            )
        return response.json()
