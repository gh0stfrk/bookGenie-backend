from pydantic import BaseModel

class UserQuery(BaseModel):
    query: str
   

class Book(BaseModel):
    book_name : str
    author_name : str
    reason : str