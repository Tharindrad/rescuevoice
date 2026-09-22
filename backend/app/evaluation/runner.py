from app.harness.engine import Harness
from app.evaluation.scenarios import scenarios


def run_evaluation():
    results=[]
    for scenario in scenarios():
        harness=Harness()
        try:
            passed=bool(scenario.run(harness))
            results.append({'id':scenario.id,'name':scenario.name,'passed':passed,'error':None})
        except Exception as exc:
            results.append({'id':scenario.id,'name':scenario.name,'passed':False,'error':str(exc)})
    passed=sum(1 for r in results if r['passed'])
    return {'total':len(results),'passed':passed,'failed':len(results)-passed,'score':round(passed/len(results),4) if results else 0,'results':results}
