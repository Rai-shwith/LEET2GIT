import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

# File handler for oauth2 log with rotation
file_handler = RotatingFileHandler("oauth2.log", maxBytes=10*1024*1024, backupCount=3)
file_handler.setFormatter(formatter)

# Only add if not already added
if not logger.hasHandlers():
    logger.addHandler(file_handler)
