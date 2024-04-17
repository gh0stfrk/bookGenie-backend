import os
import json
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")

client = OpenAI()

user_message = "I work in construction"

prompt = """
Your name is Book Genie and you are a book recommender you will recommend books based on the input from the user try to recommed books that will cover everyting that was provided in the input

In response you will only return a json object with 10 books in a json format like this
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
            "content":f"{user_message}"
        }
    ]
)

response_msg = compeletion.choices[0].message.content
parsed_json = json.loads(response_msg, )
# print(parsed_json)
print(json.dumps(parsed_json, indent=4))
# print(response_msg)

