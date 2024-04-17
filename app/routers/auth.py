import logging
from typing import Annotated
from fastapi import APIRouter, Request, Header
from fastapi import HTTPException

from ..firebase_stuff import verify_token

async def get_user_from_token(authorization: Annotated[str | None, Header(...)] = None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"Authorization":"Token"})
    token_status = verify_token(authorization)
    user_id = token_status["user_id"]
    return user_id

async def get_user_info_from_token(authorization: Annotated[str | None, Header(...)] = None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"Authorization":"Token"})
    token_status = verify_token(authorization)
    return token_status