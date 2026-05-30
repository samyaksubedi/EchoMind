from pydantic import BaseModel, EmailStr, Field


# ───────────────────────────────────────────
# Request Schemas
# ───────────────────────────────────────────


class SignUpRequest(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=6)


class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class ResendVerificationRequest(BaseModel):
    email: EmailStr


# Get Access Token
class RefreshTokenRequest(BaseModel):
    refresh_token: str
