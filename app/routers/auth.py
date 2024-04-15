from typing import Annotated
from fastapi import APIRouter, Request, Header
from ..firebase_stuff import verify_token

from app.log_manager import CreateLogger, Modules
import logging
from fastapi import HTTPException

router = APIRouter(
    prefix="/api/v1",
    tags= ["auth"]
)

logger_ = CreateLogger(Modules.auth)
logger = logger_.create_logger()

@router.post("/auth")
async def create_token(request: Request,
                       firebase_key : Annotated[str | None, Header()] = None
                       ):
    logger.info("Token created")
    headers = request.headers

    if headers.__contains__("Firebase-Key"):
        logger.log(logging.INFO, f"Firebase-Key: {headers['Firebase-Key']}")
        fkey = headers["Firebase-Key"]
        verify_token(fkey)

    logger.log(logging.INFO, f"Headers: {headers}")
    return  {"access_token": "fake-token"}

async def get_user_from_token(authorization: Annotated[str | None, Header(...)] = None):
    print(authorization)
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"Authorization":"Token"})
    token_status = verify_token(authorization)
    user_id = token_status["user_id"]
    return user_id