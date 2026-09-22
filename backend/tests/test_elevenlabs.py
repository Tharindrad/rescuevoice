import hashlib
import hmac
import json
import time

from fastapi.testclient import TestClient

from app.main import app
from app.api.elevenlabs_routes import _verify_webhook_signature

client = TestClient(app)


def test_signed_url_is_not_available_without_server_secret(monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    monkeypatch.delenv("ELEVENLABS_AGENT_ID", raising=False)
    response = client.get("/api/elevenlabs/signed-url")
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "ELEVENLABS_NOT_CONFIGURED"


def test_webhook_rejects_missing_signature(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_WEBHOOK_SECRET", "secret")
    response = client.post("/api/elevenlabs/webhooks/post-call", json={"conversation_id": "conv_demo"})
    assert response.status_code == 401


def test_webhook_signature_verification():
    secret = "secret"
    body = json.dumps({"conversation_id": "conv_demo"}).encode()
    timestamp = str(int(time.time()))
    digest = hmac.new(secret.encode(), f"{timestamp}.".encode() + body, hashlib.sha256).hexdigest()
    assert _verify_webhook_signature(body, f"t={timestamp},v0={digest}", secret)


def test_outbound_call_requires_provider_configuration(monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    monkeypatch.delenv("ELEVENLABS_AGENT_ID", raising=False)
    monkeypatch.delenv("ELEVENLABS_AGENT_PHONE_NUMBER_ID", raising=False)
    response = client.post(
        "/api/elevenlabs/outbound",
        json={"application_id": "APP-004281", "to_number": "+971501234567"},
    )
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "OUTBOUND_NOT_CONFIGURED"


def test_outbound_number_validation():
    response = client.post(
        "/api/elevenlabs/outbound",
        json={"application_id": "APP-004281", "to_number": "0501234567"},
    )
    assert response.status_code == 422
