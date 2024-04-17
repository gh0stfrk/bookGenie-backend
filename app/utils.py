import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import Request
from .models import Book
from . import root_app_path
from google_books_api_wrapper.api import GoogleBooksAPI


cred_file_path = os.path.join(root_app_path, 'creds.json')


def append_values(_values):
  """Logs data to the google sheet
    # https://docs.google.com/spreadsheets/d/1u0sdq3P5voTJkz-cYZZbmBCvRALheV6RMkx9XErY8rM/edit#gid=0
  """
  spreadsheet_id = "1u0sdq3P5voTJkz-cYZZbmBCvRALheV6RMkx9XErY8rM"
  range_name = "A1:B1"
  value_input_option = "RAW"
  creds, _ = google.auth.load_credentials_from_file(cred_file_path)
  try:
    service = build("sheets", "v4", credentials=creds)
    values = _values

    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
    return result

  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


def get_books_by_isbn(books_dict: dict) -> [Book]:
    """
    Get books by isbn
    :param books_dict: dict of books
    :return: list of books
    """
    books = []
    client = GoogleBooksAPI()
    for book in books_dict:
        google_books_search = client.search_book(isbn=book["isbn"]).get_best_match()
        if not google_books_search:
            continue
        books.append(
            Book(
                book_name=google_books_search.title,
                author_name=google_books_search.authors[0],
                reason=google_books_search.description,
                google_books_url=f"https://books.google.com/books?id={google_books_search.id}",
                isbn=google_books_search.ISBN_13,
                page_count=str(google_books_search.page_count),
                categories=google_books_search.subjects,
                cover_image=google_books_search.large_thumbnail if google_books_search.large_thumbnail else "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png",
            )
        )
    return books



def restructure_books(books_dict : dict) -> [Book]:
    """
    Parse data from OpenAI to Book Model
    :param books_dict: dict of books
    :return: list of books
    """
    book_list = []

    client = GoogleBooksAPI()

    def create_book_url(id):
        return f"https://books.google.com/books?id={id}"


    for _, book in books_dict.items():
        google_books_search = client.search_book(title=book["book_name"], author=book["author_name"]).get_best_match()
        
        if not google_books_search:
            continue
        book_list.append(Book(
            book_name=book["book_name"],
            author_name=book["author_name"],
            reason=book["reason"],
            google_books_url=create_book_url(google_books_search.id),
            isbn = google_books_search.ISBN_13,
            page_count = str(google_books_search.page_count),
            categories = google_books_search.subjects,
            cover_image = google_books_search.large_thumbnail,
        ))
    
    return book_list
    
