import os
import json
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")

prompt = """
Your name is Book Genie and you are a book recommender you will recommend books based on the input from the user try to recommed books that will cover everyting that was provided in the input

In response you will only return a json object with 10 books in a json format like this, whatever is your response it should be in json format strictly.
{
    {
        "book_name":"Book Name",
        "author_name":"Author",
        "year": "year of publishing",
        "reason": "reason of suggesting this book"
    },
    {
        "book_name":"Book Name",
        "author_name":"Author",
        "year": "year of publishing",
        "reason": "reason of suggesting this book"
    }
}
"""

def getBooks(query:str):
    """
    Dictionary of books from OpenAI

    :param query: str
    :return: dict
    """
    client = OpenAI()
    compeletion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages=[
        {
            "role":"system",
            "content": prompt
        },
        {
            "role":"user",
            "content":f"{query}"
        }
    ]
    )

    response_msg = compeletion.choices[0].message.content
    parsed_json = json.loads(response_msg)
    return parsed_json