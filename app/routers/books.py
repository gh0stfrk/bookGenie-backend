import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request

from ..models import UserQuery, FavouriteBook, AddedBook, UserModel
from ..get_books import getBooks    
from ..utils import restructure_books, get_books_by_isbn, append_values
from ..firebase_stuff import verify_token
from ..log_manager import CreateLogger, Modules
from .auth import get_user_from_token, get_user_info_from_token
from ..database import add_book, get_favourite_books, delete_book


router = APIRouter(
    prefix="/api/v1"
)


@router.post("/books", tags=["books"])
async def find_books(
    query: UserQuery,
    user_id: bool = Depends(get_user_from_token),
):
    try:
        if query.query:
            book_dict = getBooks(query.query)
            restructued_books = restructure_books(book_dict)
            try:
                log_query = str(query.query)
                log_json = json.dumps(book_dict)
                append_values([[f"{log_query}",f"{log_json}"]])
            except Exception as e:
                logger.error(f"Error during logging: {e}")
        return restructued_books
    except Exception as e:
        logger.error(f"Error during fetching books: {e}")
        logger.error(f"Error during fetching books: {book_dict}")
        raise HTTPException(status_code=500, detail=f"Internal server error : {e}")

@router.post("/favourite", tags=["books"])
async def favourite_book(book: FavouriteBook, user_id: bool = Depends(get_user_from_token)):
    """
    Check for the auth token in the header if not return 401 else add the book to firestore
    with book details from google book api.
    """
    if not book.status:
        await delete_book(book.isbn, user_id)
        return {"message": "Removed from favourites"}
    book_to_add = AddedBook(uid=user_id, isbn=book.isbn)
    added_book = await add_book(book_to_add.dict())
    return {"message": "Added to favourites"}

@router.get("/favourite/", tags=["books"])
async def get_favourite_books_(user_id = Depends(get_user_from_token)):
    """
    Get the favourite books from mongodb
    """
    books = await get_favourite_books(user_id)
    if books:
        book_objs = get_books_by_isbn(books)
        return book_objs
    return books

@router.get("/profile", response_model=UserModel)
def get_user_profile(user_details: dict = Depends(get_user_info_from_token)):
    """
    Get the user profile details
    """
    print("Executed")
    user_details = UserModel(**user_details)
    logger.info("ping")
    return user_details
