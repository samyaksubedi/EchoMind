from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/signup")
async def signup():
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
