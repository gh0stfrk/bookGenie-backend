import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from firebase_admin import auth, initialize_app
from firebase_admin import auth


load_dotenv()


FIREBASE_CONFIG=os.getenv('FIREBASE_CONFIG')
firebase_app = initialize_app(FIREBASE_CONFIG, name="auth-app")

async def verify_from_firebase(token):
    decoded_token = await auth.verify_id_token(token)
    uid = decoded_token['uid']
    return uid

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    
async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
