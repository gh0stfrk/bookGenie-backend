from firebase_admin import auth 
from .log_manager import CreateLogger, Modules
import firebase_admin

default_app = firebase_admin.initialize_app()

logger_ = CreateLogger(Modules.firebase)
logger = logger_.create_logger()

logger.info("Firebase stuff loaded")

def verify_token(token):
    """Verify tokens comming from clients
    """
    try:
        decoded_token = auth.verify_id_token(token)
        logger.info(decoded_token)
        return decoded_token
    except Exception as e:
        logger.error(e)
        return None