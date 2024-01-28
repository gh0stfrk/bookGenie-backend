from fastapi import APIRouter

from app.log_manager import CreateLogger, Modules

router = APIRouter(
    prefix="/auth",
    tags= ["auth"]
)

logger_ = CreateLogger(Modules.auth)
logger = logger_.create_logger()

@router.post("/token")
async def create_token():
    logger.info("Token created")
    return  {"access_token": "fake-token"}