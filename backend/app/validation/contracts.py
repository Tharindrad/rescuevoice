from pydantic import BaseModel, Field, field_validator

class ToolRequest(BaseModel):
    application_id: str = Field(min_length=8, max_length=40, pattern=r"^APP-[A-Z0-9-]+$")
    action: str = Field(min_length=1, max_length=80, pattern=r"^[a-z][a-z0-9_]{1,79}$")
    consent: bool = False
    idempotency_key: str = Field(min_length=8, max_length=100)

    @field_validator("action")
    @classmethod
    def no_path_chars(cls, v):
        if "/" in v or "\\" in v: raise ValueError("invalid action")
        return v

class VerificationRequest(BaseModel):
    application_id: str = Field(min_length=8, max_length=40)
    challenge_passed: bool
