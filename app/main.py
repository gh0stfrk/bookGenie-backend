from .routers import books
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .log_manager import CreateLogger, Modules


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://book-genie.vercel.app",
    "https://rapidapi.com"
]

app = FastAPI()
app.include_router(router=books.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["informational"])
async def root():
    return {
        "name": "Book Genie v0.1",
        "description": "Book Genie is a book recommendation system built with FastAPI.",
        "version": "0.1",
        "developer_info":"https://github.com/gh0stfrk"
    }


@app.get("/health", tags=["informational"])
async def health():
    return {"status": "ok"}