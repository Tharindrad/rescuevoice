import pytest

@pytest.fixture(autouse=True)
def reset_rescuevoice_state():
    from app.api.routes import harness
    harness.context._ctx.clear()
    harness.memory._cases.clear()
    harness.used_keys.clear()
    yield
    harness.context._ctx.clear()
    harness.memory._cases.clear()
    harness.used_keys.clear()
