from pydantic import BaseModel
from typing import List
class UserQuery(BaseModel):
    query: str

class AddedBook(BaseModel):
    uid: str
    isbn: str

class Book(BaseModel):
    book_name : str
    author_name : str
    reason : str
    google_books_url : str
    isbn : str
    page_count : str 
    categories : List[str]
    cover_image : str

class FavouriteBook(BaseModel):
    isbn: str
    status: bool