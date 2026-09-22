from dataclasses import dataclass, field
from typing import Any
@dataclass
class AgentContext:
    application_id:str
    verified:bool=False
    consented_actions:set[str]=field(default_factory=set)
    last_action:str|None=None
    last_error:dict[str,Any]|None=None
    attempt_count:int=0
    trace_id:str|None=None
class ContextManager:
    def __init__(self): self._ctx={}
    def get(self,application_id): return self._ctx.setdefault(application_id,AgentContext(application_id))
    def snapshot(self,application_id):
        c=self.get(application_id); return {'application_id':c.application_id,'verified':c.verified,'consented_actions':sorted(c.consented_actions),'last_action':c.last_action,'last_error':c.last_error,'attempt_count':c.attempt_count,'trace_id':c.trace_id}
