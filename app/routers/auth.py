from typing import Annotated
from fastapi import APIRouter, Request, Header
from ..firebase_stuff import verify_token

from app.log_manager import CreateLogger, Modules
import logging

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