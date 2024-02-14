from .routers import books, auth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .scheduler import scheduler
from .log_manager import CreateLogger, Modules
from .utils import clear_ip_logs

logger_ = CreateLogger(Modules.main)
logger = logger_.create_logger()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://book-genie.vercel.app"
]


app = FastAPI()
app.include_router(router=books.router)
app.include_router(router=auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if clear_ip_logs():
    logger.info("IP logs cleared")
    
scheduler.start()
logger.info("Scheduler started")

@app.middleware("http")
async def modify_request(request: Request, call_next):
    ip_addr = request.client.host
    logger.info(f"Request received from {ip_addr}")
    if await request.body():
        logger.info(f"Request body: {await request.json()}")
    return await call_next(request)


@app.get("/", tags=["informational"])
async def root():
    return {
        "name": "Book Genie v0.1",
        "description": "Book Genie is a book recommendation system built with FastAPI.",
        "version": "0.1",
        "developer_info":"https://github.com/gh0stfrk"
    }