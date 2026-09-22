from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health(): assert client.get('/api/health').json()['harness']=='enabled'
def test_context_verification_required():
 r=client.post('/api/actions/execute',json={'application_id':'APP-004281','action':'upload_corrected_passport','consent':True,'idempotency_key':'verifyfirst-001'}); assert r.json()['error']['code']=='VERIFICATION_REQUIRED'
def test_verification_and_allowed_action():
 client.post('/api/verify',json={'application_id':'APP-004281','challenge_passed':True})
 r=client.post('/api/actions/execute',json={'application_id':'APP-004281','action':'upload_corrected_passport','consent':True,'idempotency_key':'action-001'}); assert r.json()['ok'] is True
def test_dangerous_action_blocked():
 client.post('/api/verify',json={'application_id':'APP-004281','challenge_passed':True})
 r=client.post('/api/actions/execute',json={'application_id':'APP-004281','action':'approve_application','consent':True,'idempotency_key':'danger-001'}); assert r.json()['error']['code']=='POLICY_DENIED' and r.json()['error']['human_required'] is True
def test_invalid_tool_schema():
 r=client.post('/api/actions/execute',json={'application_id':'bad','action':'x','consent':True,'idempotency_key':'bad-001'}); assert r.status_code==422
def test_memory_audit_state():
 client.post('/api/verify',json={'application_id':'APP-004281','challenge_passed':True})
 r=client.get('/api/memory/APP-004281').json(); assert 'audit_events' in r
def test_idempotent_replay():
 client.post('/api/verify',json={'application_id':'APP-004282','challenge_passed':True})
 payload={'application_id':'APP-004282','action':'book_appointment','consent':True,'idempotency_key':'same-key-001'}
 first=client.post('/api/actions/execute',json=payload).json(); second=client.post('/api/actions/execute',json=payload).json(); assert first['ok'] and second['replayed']
def test_loop_stops_on_non_retryable():
 client.post('/api/verify',json={'application_id':'APP-004283','challenge_passed':True})
 r=client.post('/api/loop/run',json={'application_id':'APP-004283','action':'approve_application','consent':True,'idempotency_key':'loop-001'}).json(); assert len(r['history'])==1
