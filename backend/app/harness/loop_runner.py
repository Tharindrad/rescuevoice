from app.loop.engine import LoopController

class HarnessLoop:
    def __init__(self,harness):
        self.harness=harness
        self.loop=LoopController(2)

    def run(self,application_id,action,consent,idempotency_key):
        def act(attempt):
            return self.harness.execute(
                application_id, action, consent, f"{idempotency_key}-{attempt}"
            )

        def judge(result,attempt):
            err=result.get("error",{})
            if not err:
                return {"retry":False,"reason":"success"}
            return {
                "retry":bool(err.get("retryable")) and attempt<2,
                "reason":"retryable_error" if err.get("retryable") else "non_retryable_error"
            }

        result=self.loop.run(act,should_retry=judge)
        history=result.get("history", [])
        terminal_error=history[-1].get("error") if history else None
        result["ok"] = not bool(terminal_error)
        result["human_required"] = bool(terminal_error and terminal_error.get("human_required"))
        if terminal_error:
            result["error"] = terminal_error
        return result
