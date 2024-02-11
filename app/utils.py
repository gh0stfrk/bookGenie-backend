from fastapi import Request
from app.database import IPLog, SessionLocal
from .models import Book
from google_books_api_wrapper.api import GoogleBooksAPI



def restructure_books(books_dict : dict):
    """
    Create a static return model by parsing returns from
    openapi
    """
    book_obj = []

    client = GoogleBooksAPI()

    def create_book_url(id):
        # Add this method to GoogleBooksAPI
        return f"https://books.google.com/books?id={id}"


    for _, book in books_dict.items():
        google_books_search = client.search_book(title=book["book_name"], author=book["author_name"]).get_best_match()

        book_obj.append(Book(
            book_name=book["book_name"],
            author_name=book["author_name"],
            reason=book["reason"],
            google_books_url=create_book_url(google_books_search.id),
            isbn = google_books_search.ISBN_13,
            page_count = str(google_books_search.page_count),
            categories = google_books_search.subjects,
            cover_image = google_books_search.large_thumbnail,
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