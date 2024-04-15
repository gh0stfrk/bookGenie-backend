import os 
import logging

from enum import Enum
from main import root_path
from logging.handlers import TimedRotatingFileHandler
from logging import FileHandler


# Add module name to create new loggers
class Modules(Enum):
    main = "main"
    database = "database"
    auth = "auth"
    books = "books"
    firebase = "firebase"


class CreateLogger():
    """ Creates a logger for a module with the appropriate module name. """
    def __init__(self, module_name : Modules):
        """
        module_name : str
        """
        self.module_name = module_name.value
        root_app_path = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(root_path, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = os.path.join(log_dir, f"{self.module_name}.log")

    def create_logger(self):
        logger = logging.getLogger(self.module_name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler = FileHandler(filename=self.log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger







