from app.observability.logger import event,new_trace_id

class LoopController:
    def __init__(self,max_attempts=2): self.max_attempts=max_attempts
    def run(self, action_fn, *, should_retry):
        trace=new_trace_id(); history=[]
        for attempt in range(1,self.max_attempts+1):
            event("act",trace,attempt=attempt); result=action_fn(attempt); history.append(result)
            event("observe",trace,attempt=attempt,ok=result.get("ok",False),error=result.get("error"))
            if result.get("ok"): event("stop",trace,reason="success",attempts=attempt); return {"trace_id":trace,"status":"stopped","history":history}
            decision=should_retry(result,attempt)
            event("judge",trace,attempt=attempt,retry=decision["retry"],reason=decision["reason"])
            if not decision["retry"]: event("stop",trace,reason=decision["reason"],attempts=attempt); return {"trace_id":trace,"status":"stopped","history":history}
            event("adjust",trace,attempt=attempt,strategy=decision.get("strategy","bounded_retry"))
        event("stop",trace,reason="retry_limit",attempts=self.max_attempts); return {"trace_id":trace,"status":"stopped","history":history}
