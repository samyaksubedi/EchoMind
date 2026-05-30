from fastapi import APIRouter
from app.schemas.auth_schema import SignUpRequest

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    "/signup",
    description="Registers user into the Database and sends email confirmation mail.",
)
async def signup(body: SignUpRequest):
    return {"email": body.email, "password": body.password}


@router.post(
    "/resend-verification",
    description="Registers user into the Database and sends email confirmation mail.",
)
async def resend_verification_token():
    return {"message": "Signup route"}


@router.post("/signin")
async def signin():
    return {"message": "Signin route"}


@router.post("/signout")
async def signout():
    return {"message": "Signout route"}


@router.post("/refresh")
async def refresh():
    return {"message": "Refresh token route"}


@router.get("/me")
async def get_me():
    return {"message": "Current user route"}
