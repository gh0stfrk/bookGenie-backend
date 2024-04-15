import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request

from ..models import UserQuery, FavouriteBook, AddedBook
from ..get_books import getBooks    
from ..utils import restructure_books
from ..write_to_sheets import append_values
from ..firebase_stuff import verify_token
from ..log_manager import CreateLogger, Modules
from .auth import get_user_from_token
from ..database import add_book

logger_ = CreateLogger(Modules.books)
logger = logger_.create_logger()

router = APIRouter(
    prefix="/api/v1"
)


@router.post("/books", tags=["books"])
async def find_books(
    query: UserQuery,
    request: Request  
):
    print(query)
    try:
        ## TODO : Remove before deployingd
        # Working with test request before deploying 
        if request.headers.__contains__("Dummy"):
            books = """{"book1": {"book_name": "Bigger Leaner Stronger", "author_name": "Michael Matthews", "year": "2012", "reason": "This book provides comprehensive guidance on building muscle, losing fat, and getting strong through effective workout and nutrition strategies."}, "book2": {"book_name": "Strength Training Anatomy", "author_name": "Frederic Delavier", "year": "2001", "reason": "This book offers detailed illustrations and explanations of strength training exercises, making it an excellent resource for understanding the mechanics of bodybuilding."}, "book3": {"book_name": "The New Rules of Lifting for Women", "author_name": "Lou Schuler and Alwyn Cosgrove", "year": "2007", "reason": "This book challenges traditional approaches to female strength training, providing a fresh perspective on effective workouts and lifting techniques."}, "book4": {"book_name": "Arnold: The Education of a Bodybuilder", "author_name": "Arnold Schwarzenegger and Douglas Kent Hall", "year": "1977", "reason": "Arnold Schwarzenegger's autobiography offers insights into his bodybuilding journey and the mindset required to excel in the sport."}, "book5": {"book_name": "The Bodybuilding.com Guide to Your Best Body", "author_name": "Kris Gethin", "year": "2013", "reason": "This book provides a comprehensive guide to bodybuilding, including workout plans, nutrition advice, and motivational strategies."}}"""
            try:
                j_book = json.loads(books)
                r_books = restructure_books(j_book)
            except Exception as e:
                raise e
            return r_books
        
        if query.query:
            book_dict = getBooks(query.query)
            restructued_books = restructure_books(book_dict)
            log_query = str(query.query)
            log_json = json.dumps(book_dict)
            try:
                append_values([[f"{log_query}",f"{log_json}"]])
            except Exception as e:
                logger.error(f"Error during logging: {e}")

        return restructued_books

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error : {e}")

@router.post("/favourite", tags=["books"])
async def favourite_book(book: FavouriteBook, user_id: bool = Depends(get_user_from_token)):
    """
    Check for the auth token in the header if not return 401 else add the book to firestore
    with book details from google book api.
    """
    print(book)
    print(user_id)
    if not book.status:
        return {"message": "Removed from favourites"}
    book_to_add = AddedBook(uid=user_id, isbn=book.isbn)
    added_book = await add_book(book_to_add)
    print(added_book)
    return {"message": "Added to favourites"}