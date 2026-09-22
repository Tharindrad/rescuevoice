from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.harness.engine import Harness
from app.harness.loop_runner import HarnessLoop
from app.tools.government import get_application,get_issue
from app.validation.contracts import ToolRequest,VerificationRequest
router=APIRouter(); harness=Harness(); loop=HarnessLoop(harness)
class ActionRequest(ToolRequest): pass
@router.get('/health')
def health(): return {'status':'ok','service':'rescuevoice-api','harness':'enabled'}
@router.get('/applications')
def applications():
    from app.tools.government import GOVERNMENT
    return list(GOVERNMENT.values())

@router.get('/applications/{application_id}')
def application(application_id:str): return get_application(application_id) or {'error':{'code':'NOT_FOUND','message':'Application not found'}}
@router.get('/applications/{application_id}/issue')
def issue(application_id:str): return get_issue(application_id) or {'error':{'code':'NOT_FOUND','message':'Application not found'}}
@router.post('/verify')
def verify(req:VerificationRequest): return harness.verify(req.application_id,req.challenge_passed)
@router.post('/policy/check')
def policy(req:ActionRequest): return harness.check(req.application_id,req.action,req.consent)
@router.post('/actions/execute')
def execute(req:ActionRequest): return harness.execute(req.application_id,req.action,req.consent,req.idempotency_key)
@router.post('/loop/run')
def run_loop(req:ActionRequest): return loop.run(req.application_id,req.action,req.consent,req.idempotency_key)
@router.get('/memory/{application_id}')
def memory(application_id:str): return harness.memory.snapshot(application_id)
