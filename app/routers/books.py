from fastapi import APIRouter
from ..models import UserQuery
from ..get_books import getBooks    
from ..utils import restructure_books
from ..write_to_sheets import append_values
import json


router = APIRouter(
    prefix="/api/v1"
)


@router.post("/get_books", tags=["books"])
def find_books(query: UserQuery):

    if query.query:
        book_dict = getBooks(query.query)
        restructued_books = restructure_books(book_dict)

        log_query = str(query.query)
        log_json = json.dumps(book_dict)
        append_values([
            [
            f"{log_query}",
            f"{log_json}"
            ]
        ])
    
    return restructued_books
