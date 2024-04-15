from fastapi import Request
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
    
