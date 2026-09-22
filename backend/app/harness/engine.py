from app.context.manager import ContextManager
from app.memory.store import MemoryStore
from app.observability.logger import event,new_trace_id
from app.policy.rules import evaluate
from app.tools.government import get_application, execute
from app.errors.types import AgentError

class Harness:
    def __init__(self): self.context=ContextManager(); self.memory=MemoryStore(); self.used_keys=set()
    def _audit(self, application_id, trace_id, event_type, **fields):
        record=event(event_type,trace_id,application_id=application_id,**fields)
        self.memory.get(application_id).audit_events.append(record)
        return record
    def verify(self, application_id, challenge_passed):
        trace=new_trace_id(); ctx=self.context.get(application_id); ctx.trace_id=trace; ctx.verified=bool(challenge_passed)
        if not ctx.verified:
            ctx.consented_actions.clear()
        self._audit(application_id,trace,'verification',passed=ctx.verified)
        return {'ok':ctx.verified,'verified':ctx.verified,'trace_id':trace,'error':None if ctx.verified else AgentError('VERIFICATION_FAILED','Verification did not pass.',False,True).as_dict()}
    def check(self, application_id, action, consent=False):
        trace=self.context.get(application_id).trace_id or new_trace_id(); case=get_application(application_id)
        if not case: return {'allowed':False,'code':'NOT_FOUND','reason':'Application not found','human_required':False,'trace_id':trace}
        ctx=self.context.get(application_id); result=evaluate(action,case,verified=ctx.verified,consent=consent)
        self._audit(application_id,trace,'policy_check',action=action,**result)
        return {**result,'trace_id':trace}
    def execute(self, application_id, action, consent, idempotency_key):
        trace=self.context.get(application_id).trace_id or new_trace_id()
        if idempotency_key in self.used_keys:
            return {'ok':True,'replayed':True,'trace_id':trace,'result':{'message':'Idempotent replay; no duplicate action executed.'}}
        policy=self.check(application_id,action,consent)
        if not policy['allowed']:
            if policy.get('human_required'): self.memory.get(application_id).escalation=True
            err=AgentError(policy['code'],policy['reason'],policy.get('retryable',False),policy.get('human_required',False)).as_dict()
            self._audit(application_id,trace,'action_blocked',action=action,error=err)
            return {'ok':False,'trace_id':trace,'error':err}
        self.memory.record_consent(application_id,action); self.context.get(application_id).consented_actions.add(action)
        self.used_keys.add(idempotency_key)
        result=execute(action,application_id,idempotency_key)
        mem=self.memory.get(application_id)
        if result['ok']: mem.completed_actions.append(action)
        else: mem.failed_actions.append(action)
        self._audit(application_id,trace,'tool_result',action=action,ok=result['ok'],result=result)
        return {'ok':result['ok'],'trace_id':trace,'result':result,'memory':self.memory.snapshot(application_id)}
