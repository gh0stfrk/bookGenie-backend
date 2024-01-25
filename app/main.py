import os
import logging
from main import root_path
from .routers import books, auth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import TimedRotatingFileHandler

root_app_path = os.path.dirname(os.path.abspath(__file__))

log_dir = os.path.join(root_path, "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "app.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
handler.setFormatter(formatter)
logger.addHandler(handler)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
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

@app.middleware("http")
async def modify_request(request: Request, call_next):
    ip_addr = request.client.host
    print(request.url.path)
    logger.info(f"Request received from {ip_addr}")
    if request.body():
        logger.info(f"Request body: {request.body}")
    return await call_next(request)


@app.get("/", tags=["informational"])
async def root():
    return {
        "name": "Book Genie v0.1",
        "description": "Book Genie is a book recommendation system built with FastAPI.",
        "version": "0.1",
        "developer_info":"https://github.com/gh0stfrk"
    }