import logging

import os

# Ensure the LOGS directory exists
log_dir = "LOGS"
log_file = "scripts.log"
os.makedirs(log_dir, exist_ok=True)  # Create the directory if it does not exist

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, log_file), mode="a"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)