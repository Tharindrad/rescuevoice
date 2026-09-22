import os
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.integrations.elevenlabs.client import ElevenLabsClient, ElevenLabsAPIError, ElevenLabsConfigurationError
from app.tools.government import GOVERNMENT
from app.observability.logger import event, new_trace_id

router = APIRouter()

E164 = re.compile(r"^\+[1-9]\d{7,14}$")

class OutboundCallRequest(BaseModel):
    application_id: str = Field(pattern=r"^APP-[A-Z0-9-]+$")
    to_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    call_recording_enabled: bool = True

@router.post("/outbound-call")
def outbound_call(req: OutboundCallRequest):
    trace_id = new_trace_id()
    app = GOVERNMENT.get(req.application_id)
    if not app:
        raise HTTPException(status_code=404, detail={"code":"APPLICATION_NOT_FOUND","trace_id":trace_id})
    if not E164.fullmatch(req.to_number):
        raise HTTPException(status_code=422, detail={"code":"INVALID_E164","trace_id":trace_id})

    agent_id = os.getenv("ELEVENLABS_AGENT_ID")
    phone_id = os.getenv("ELEVENLABS_AGENT_PHONE_NUMBER_ID")
    if not agent_id or not phone_id:
        raise HTTPException(
            status_code=503,
            detail={"code":"OUTBOUND_CALL_NOT_CONFIGURED","message":"ELEVENLABS_AGENT_ID and ELEVENLABS_AGENT_PHONE_NUMBER_ID are required.","trace_id":trace_id},
        )

    try:
        result = ElevenLabsClient().outbound_call(
            agent_id=agent_id,
            agent_phone_number_id=phone_id,
            to_number=req.to_number,
            application_id=req.application_id,
            applicant_name=app["applicant"],
            language=app["language"],
            call_recording_enabled=req.call_recording_enabled,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={"code":"INVALID_E164","message":str(exc),"trace_id":trace_id})
    except ElevenLabsConfigurationError as exc:
        event("twilio_outbound_config_error", trace_id, error=str(exc))
        raise HTTPException(status_code=503, detail={"code":"ELEVENLABS_NOT_CONFIGURED","trace_id":trace_id})
    except ElevenLabsAPIError as exc:
        event("twilio_outbound_upstream_error", trace_id, error=str(exc))
        raise HTTPException(status_code=502, detail={"code":"OUTBOUND_CALL_FAILED","trace_id":trace_id})

    event("twilio_outbound_call_started", trace_id, application_id=req.application_id, conversation_id=result.get("conversation_id"), call_sid=result.get("callSid"))
    return {
        "ok": True,
        "provider": "elevenlabs_twilio",
        "trace_id": trace_id,
        "application_id": req.application_id,
        "conversation_id": result.get("conversation_id"),
        "call_sid": result.get("callSid"),
        "message": result.get("message"),
    }
