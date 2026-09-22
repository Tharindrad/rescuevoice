import hashlib
import hmac
import os
import time
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

from app.integrations.elevenlabs.client import (
    ElevenLabsAPIError,
    ElevenLabsClient,
    ElevenLabsConfigurationError,
)
from app.observability.logger import event, new_trace_id

router = APIRouter()


class SignedURLResponse(BaseModel):
    signedUrl: str
    provider: str = "elevenlabs"


def _verify_webhook_signature(raw_body: bytes, signature: str | None, secret: str | None) -> bool:
    if not signature or not secret:
        return False
    # ElevenLabs signatures use a timestamped HMAC value. Keep verification server-side.
    # Accept common `t=<timestamp>,v0=<digest>` form and reject stale requests.
    parts = dict(item.split("=", 1) for item in signature.split(",") if "=" in item)
    timestamp = parts.get("t")
    digest = parts.get("v0")
    if not timestamp or not digest:
        return False
    try:
        ts = int(timestamp)
    except ValueError:
        return False
    if abs(time.time() - ts) > 300:
        return False
    signed = f"{timestamp}.".encode() + raw_body
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, digest)


@router.get("/signed-url", response_model=SignedURLResponse)
def signed_url():
    trace_id = new_trace_id()
    try:
        result = ElevenLabsClient().get_signed_url(include_conversation_id=True)
    except ElevenLabsConfigurationError as exc:
        event("elevenlabs_config_error", trace_id, error=str(exc))
        raise HTTPException(status_code=503, detail={"code": "ELEVENLABS_NOT_CONFIGURED", "trace_id": trace_id})
    except ElevenLabsAPIError as exc:
        event("elevenlabs_api_error", trace_id, error=str(exc))
        raise HTTPException(status_code=502, detail={"code": "ELEVENLABS_UPSTREAM_ERROR", "trace_id": trace_id})
    event("elevenlabs_signed_url_issued", trace_id)
    return SignedURLResponse(signedUrl=result["signed_url"])


@router.post("/webhooks/post-call")
async def post_call_webhook(request: Request, elevenlabs_signature: str | None = Header(default=None)):
    raw_body = await request.body()
    secret = os.getenv("ELEVENLABS_WEBHOOK_SECRET")
    if not _verify_webhook_signature(raw_body, elevenlabs_signature, secret):
        raise HTTPException(status_code=401, detail={"code": "INVALID_WEBHOOK_SIGNATURE"})

    payload: Any = await request.json()
    trace_id = new_trace_id()
    event("elevenlabs_post_call_received", trace_id, conversation_id=payload.get("conversation_id"))
    # Store/forward the payload through the audit pipeline in the next integration milestone.
    return {"ok": True, "trace_id": trace_id}


class OutboundCallRequest(BaseModel):
    application_id: str
    to_number: str
    call_recording_enabled: bool = True

@router.post("/outbound")
def outbound_alias(req: OutboundCallRequest):
    trace_id = new_trace_id()
    if not req.to_number.startswith("+"):
        raise HTTPException(status_code=422, detail={"code": "INVALID_E164", "trace_id": trace_id})
    if not os.getenv("ELEVENLABS_API_KEY") or not os.getenv("ELEVENLABS_AGENT_ID") or not os.getenv("ELEVENLABS_AGENT_PHONE_NUMBER_ID"):
        raise HTTPException(status_code=503, detail={"code": "OUTBOUND_NOT_CONFIGURED", "trace_id": trace_id})
    # Provider invocation is deliberately delegated to the native outbound endpoint.
    from app.api.outbound_routes import outbound_call
    return outbound_call(req)
