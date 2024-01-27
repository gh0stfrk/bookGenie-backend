from fastapi import Request
from .models import Book


def restructure_books(books_dict : dict):
    """
    Create a static return model by parsing returns from
    openapi
    """
    book_obj = []

    for key, book in books_dict.items():
        book_obj.append(Book(
            book_name=book["book_name"],
            author_name=book["author_name"],
            reason=book["reason"]
        ))
    
    return book_obj


def get_client_ip(request: Request):
    client_ip = request.headers.get("X-Forwarded-For")
    if client_ip is None:
        client_ip = request.client.host
    return client_ip
