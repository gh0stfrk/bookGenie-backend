from fastapi import APIRouter
from ..models import UserQuery
from ..utils import restructure_books

from ..get_books import getBooks

router = APIRouter(
    prefix="/api/v1"
)


@router.post("/get_books", tags=["books"])
def find_books(query: UserQuery):
    if query.query:
        book_dict = getBooks(query.query)
        book_dict = restructure_books(book_dict)
    return book_dict
