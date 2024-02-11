import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request
from app.database import IPLog, SessionLocal, get_db

from ..models import UserQuery
from ..get_books import getBooks    
from ..utils import get_client_ip, restructure_books
from ..write_to_sheets import append_values
from ..firebase_stuff import verify_token
from ..log_manager import CreateLogger, Modules


logger_ = CreateLogger(Modules.books)
logger = logger_.create_logger()

router = APIRouter(
    prefix="/api/v1"
)

async def check_rate_limit(request: Request, session: SessionLocal = Depends(get_db)): # type: ignore
    ip_address = get_client_ip(request) 
    logger.log(logging.INFO, f"IP address: {ip_address}")

    headers = request.headers
    if headers.__contains__("IdToken"):
        logger.log(logging.INFO, f"IdToken: {headers['IdToken']}")
        fkey = headers["IdToken"]
        verify_token(fkey)
        return
    
    if headers.__contains__("Dummy"):
        return
    
    ip_log = (
        session.query(IPLog)
        .filter_by(ip_address=ip_address)
        .first()
    )

    if ip_log and ip_log.request_count >= 3:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    if not ip_log:
        ip_log = IPLog(ip_address=ip_address, request_count=0)
        session.add(ip_log)

    ip_log.request_count = ip_log.request_count + 1

    session.commit()



@router.post("/books", tags=["books"])
async def find_books(
    query: UserQuery,
    request: Request,  
    check_rate_limit = Depends(check_rate_limit)  
):
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
async def favourite_book():
    """
    Check for the auth token in the header if not return 401 else add the book to firestore
    with book details from google book api.
    """
    return {"message": "Favourite book endpoint"}