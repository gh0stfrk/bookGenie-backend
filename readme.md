# Book Genie 
API's for book genie 
Python 3.11.7

# Featuers 
- Rate limitting 
- Allow more queries after signup with google

# Endpoints

getbookRecommendations() POST
Req ["query",auth_token|temp_user,]
{
    returns a list of books with required keys
    {
        "bookName",
        "author",
        "coverImg:optional",
        "description",
        "affiliate_link",
    }
}


# Steps to return a bookRecommendations JSON obj

- 1) Get the msg from the user to suggest books
- 2) Get a list of books from OpenAi API
- 3) Find affliate links to those books from ebooks.com
- 4) Create a new object with all necessary items to dispay user books


# Sample flow 
-