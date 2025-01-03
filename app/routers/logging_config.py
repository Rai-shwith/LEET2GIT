import logging
import os

# Ensure the LOGS directory exists
log_dir = "LOGS"
log_file = "oauth2.log"
os.makedirs(log_dir, exist_ok=True)  # Create the directory if it does not exist

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
file_handler = logging.FileHandler(os.path.join(log_dir, log_file),"a")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)