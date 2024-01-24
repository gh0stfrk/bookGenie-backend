from fastapi import FastAPI, Request
from .routers import books, auth
from fastapi.middleware.cors import CORSMiddleware

import logging

logging.basicConfig(
    level=logging.DEBUG
)



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
    return await call_next(request)


@app.get("/", tags=["informational"])
async def root():
    return {
        "name": "Book Genie v0.1",
        "description": "Book Genie is a book recommendation system built with FastAPI.",
        "version": "0.1",
        "developer_info":"https://github.com/gh0stfrk"
    }