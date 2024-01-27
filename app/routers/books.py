import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
import jwt
from app.database import IPLog, SessionLocal, get_db

from ..models import UserQuery
from ..get_books import getBooks    
from ..utils import get_client_ip, restructure_books
from ..write_to_sheets import append_values
import json


router = APIRouter(
    prefix="/api/v1"
)

async def check_rate_limit(request: Request, session: SessionLocal = Depends(get_db)):
    ip_address = get_client_ip(request)  # Replace with your IP retrieval logic


    # Check for authentication cookie
    auth_cookie = request.cookies.get("auth_cookie")  # Replace with your actual cookie name
    if auth_cookie:
        # Validate the JWT token (replace with your token validation logic)
        try:
            payload = jwt.decode(auth_cookie, "your_secret_key", algorithms=["HS256"])
            # If token is valid, skip rate limiting
            return
        except jwt.exceptions.DecodeError:
            pass  # Handle invalid token gracefully (e.g., log or raise an error)

    today = datetime.date.today()

    ip_log = (
        session.query(IPLog)
        .filter_by(ip_address=ip_address)
        .first()
    )

    logging.error(f"ip_log value {ip_log}")

    if ip_log and ip_log.request_count >= 3:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    logging.error(f"IP log updated: {ip_log}")  

    if not ip_log:
        ip_log = IPLog(ip_address=ip_address, request_count=0)
        session.add(ip_log)

    ip_log.request_count = ip_log.request_count + 1

    session.commit()


@router.post("/get_books", tags=["books"])
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
                # Handle logging errors gracefully
                print(f"Error during logging: {e}")

        return restructued_books

    except Exception as e:
        # Handle other endpoint-related errors
        raise HTTPException(status_code=500, detail="Internal server error")

