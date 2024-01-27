from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags= ["auth"]
)


@router.post("/token")
async def create_token():
    return  {"access_token": "fake-token"}