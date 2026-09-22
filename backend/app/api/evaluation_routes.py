from fastapi import APIRouter
from app.evaluation.runner import run_evaluation
from app.evaluation.adversarial_eval import run_all_adversarial_tests

router=APIRouter()

@router.post('/run')
def run():
    return run_evaluation()

@router.post('/adversarial')
def adversarial():
    return run_all_adversarial_tests()

@router.get("/e2e/status")
def e2e_status():
    return {
        "status": "ready",
        "provider_independent": True,
        "primary_case": "APP-004281",
        "escalation_case": "APP-004283",
        "required_providers": ["ElevenLabs", "Twilio"],
        "control_plane": "RescueVoice Harness"
    }
