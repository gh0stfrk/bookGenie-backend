from fastapi import Request
from app.database import IPLog, SessionLocal
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
    """Get client ip address from request headers.
    """
    client_ip = request.headers.get("X-Forwarded-For")
    if client_ip is None:
        client_ip = request.client.host
    return client_ip


def clear_ip_logs():
    """Clears ip_logs in the database
    """
    try:
        session = SessionLocal()
        session.query(IPLog).delete()
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(e)
        return False