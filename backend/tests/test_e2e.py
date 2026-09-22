import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_e2e_correction_path():
    # 1. Government exception is available
    case = client.get("/api/applications/APP-004281")
    assert case.status_code == 200
    data = case.json()
    assert data["allowed_actions"]

    # 2. Verification
    verified = client.post("/api/verify", json={
        "application_id": "APP-004281",
        "challenge_passed": True
    })
    assert verified.status_code == 200
    assert verified.json()["verified"] is True

    # 3. Policy gate before action
    action = data["allowed_actions"][0]
    policy = client.post("/api/policy/check", json={
        "application_id": "APP-004281",
        "action": action,
        "consent": True,
        "idempotency_key": "e2e-policy-004281"
    })
    assert policy.status_code == 200
    assert policy.json()["allowed"] is True

    # 4. Execute through Harness
    executed = client.post("/api/actions/execute", json={
        "application_id": "APP-004281",
        "action": action,
        "consent": True,
        "idempotency_key": "e2e-action-004281"
    })
    assert executed.status_code == 200
    result = executed.json()
    assert result["ok"] is True
    assert result.get("final_decision_owner") == "government_officer" or result.get("result", {}).get("final_decision_owner") == "government_officer"

def test_e2e_dispute_safe_stop():
    case = client.get("/api/applications/APP-004283")
    assert case.status_code == 200
    data = case.json()
    assert data["allowed_actions"] == []

    loop = client.post("/api/loop/run", json={
        "application_id": "APP-004283",
        "action": "change_final_decision",
        "consent": True,
        "idempotency_key": "e2e-dispute-004283"
    })
    assert loop.status_code in (200, 403)
    body = loop.json()
    assert body.get("ok") is False or body.get("human_required") is True

def test_e2e_idempotency_replay():
    client.post("/api/verify", json={"application_id": "APP-004281", "challenge_passed": True})
    payload = {
        "application_id": "APP-004281",
        "action": "upload_corrected_passport",
        "consent": True,
        "idempotency_key": "e2e-replay-004281"
    }
    first = client.post("/api/actions/execute", json=payload)
    second = client.post("/api/actions/execute", json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json().get("replayed") is True or second.json().get("idempotent_replay") is True
