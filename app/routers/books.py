import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request

from ..models import UserQuery
from ..get_books import getBooks    
from ..utils import restructure_books
from ..write_to_sheets import append_values



router = APIRouter(
    prefix="/api/v1"
)


@router.post("/books", tags=["books"])
async def find_books(
    query: UserQuery,
    request: Request
):
    try:
        if query.query:
            book_dict = getBooks(query.query)
            restructued_books = restructure_books(book_dict)
            log_query = str(query.query)
            log_json = json.dumps(book_dict)

            try:
                append_values([[f"{log_query}",f"{log_json}"]])
            except Exception as e:
                pass

        return restructued_books

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error : {e}")
