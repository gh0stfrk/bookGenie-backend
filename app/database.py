import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

passwd = os.getenv("MONGO_PASSWORD")
user = os.getenv("MONGO_USER")

MONGO_URL = f"mongodb+srv://{user}:{passwd}@cluster0.hlgdohp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.bookgenie
fav_books = database.get_collection("fav_books")


def favourite_books_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "uid": book["uid"],
        "isbn" : book["isbn"],
    }
    
async def add_book(book_data: dict):
    book = await fav_books.insert_one(book_data)
    new_book = await fav_books.find_one({"_id": book.inserted_id})
    return favourite_books_helper(new_book)

async def get_favourite_books(user_id: str):
    books = []
    async for book in fav_books.find({"uid": user_id}):
        books.append(favourite_books_helper(book))
    return books

async def delete_book(book_id: str, user_id: str):
    await fav_books.delete_one({"isbn": book_id, "uid": user_id})