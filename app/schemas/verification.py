from pydantic import BaseModel, EmailStr, Field


class VerifyEmailRequest(BaseModel):
    code: str = Field(min_length=6, max_length=6)


class ResendVerificationRequest(BaseModel):
    email: EmailStr
    

class VerificationResponse(BaseModel):
    message: str