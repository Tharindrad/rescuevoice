from app.evaluation.adversarial_eval import AdversarialEvaluator, run_all_adversarial_tests

def _results():
    return AdversarialEvaluator().run_all()

def test_wrong_identity():
    assert _results()[0].status == "PASS"

def test_unpermitted_action():
    assert _results()[1].status == "PASS"

def test_legal_dispute():
    assert _results()[2].status == "PASS"

def test_prompt_injection():
    assert _results()[3].status == "PASS"

def test_no_consent():
    assert _results()[4].status == "PASS"

def test_gov_timeout():
    assert _results()[5].status == "PASS"

def test_elevenlabs_disconnect():
    assert _results()[6].status == "PASS"

def test_twilio_failure():
    assert _results()[7].status == "PASS"

def test_duplicate_retry():
    assert _results()[8].status == "PASS"

def test_repeated_wrong_id():
    assert _results()[9].status == "PASS"

def test_distress():
    assert _results()[10].status == "PASS"

def test_unrecognized_rejection():
    assert _results()[11].status == "PASS"

def test_language_switch():
    assert _results()[12].status == "PASS"

def test_all_adversarial_tests_pass():
    report = run_all_adversarial_tests()
    assert report["total"] == 13
    assert report["failed"] == 0
    assert report["pass_rate"] == 100.0
