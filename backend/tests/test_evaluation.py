from app.evaluation.runner import run_evaluation


def test_agent_evaluation_suite_passes():
    report=run_evaluation()
    assert report['total'] == 8
    assert report['failed'] == 0
    assert report['score'] == 1.0
