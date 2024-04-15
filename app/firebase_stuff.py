import os
import firebase_admin
from . import root_app_path
from firebase_admin import auth
from firebase_admin import credentials
from .log_manager import CreateLogger, Modules
from fastapi import HTTPException

cred_file = os.path.join(root_app_path, "creds.json")
creds = credentials.Certificate(cred_file)

default_app = firebase_admin.initialize_app(credential=creds)

logger_ = CreateLogger(Modules.firebase)
logger = logger_.create_logger()

logger.info("Firebase stuff loaded")

def verify_token(token):
    """Verify tokens comming from clients
    """
    try:
        decoded_token = auth.verify_id_token(token)
        
        uid = decoded_token['uid']
        username = decoded_token['name']
        email = decoded_token['email']
        
        logger.info(f"UID: {uid}")
        logger.info(f"Username: {username}")
        logger.info(f"Email: {email}")

        logger.info(decoded_token)
        return decoded_token
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=401, detail=f"{e}", headers={"Authorization":"Token"})