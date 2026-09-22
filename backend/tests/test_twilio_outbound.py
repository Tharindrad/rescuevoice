import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_outbound_requires_config():
    os.environ.pop("ELEVENLABS_AGENT_ID", None)
    os.environ.pop("ELEVENLABS_AGENT_PHONE_NUMBER_ID", None)
    r=client.post("/api/outbound-call",json={
        "application_id":"APP-004281","to_number":"+971500000000","call_recording_enabled":True
    })
    assert r.status_code==503
    assert r.json()["detail"]["code"]=="OUTBOUND_CALL_NOT_CONFIGURED"

def test_outbound_rejects_bad_number():
    r=client.post("/api/outbound-call",json={
        "application_id":"APP-004281","to_number":"0500000000"
    })
    assert r.status_code==422

def test_outbound_unknown_case():
    r=client.post("/api/outbound-call",json={
        "application_id":"APP-DOES-NOT-EXIST","to_number":"+971500000000"
    })
    assert r.status_code==404
