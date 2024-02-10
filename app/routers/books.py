import datetime
import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request
import jwt
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

async def check_rate_limit(request: Request, session: SessionLocal = Depends(get_db)):
    ip_address = get_client_ip(request) 
    logger.log(logging.INFO, f"IP address: {ip_address}")

    headers = request.headers
    if headers.__contains__("IdToken"):
        logger.log(logging.INFO, f"IdToken: {headers['IdToken']}")
        fkey = headers["IdToken"]
        verify_token(fkey)

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
        if query.query:
            book_dict = getBooks(query.query)
            restructued_books = restructure_books(book_dict)

            log_query = str(query.query)
            log_json = json.dumps(book_dict)

            # Append values to log, handling potential errors
            try:
                append_values([
                    [
                        f"{log_query}",
                        f"{log_json}"
                    ]
                ])
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