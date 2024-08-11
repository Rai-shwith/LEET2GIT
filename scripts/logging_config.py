import logging
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s-%(message)s',
                    handlers=[logging.FileHandler("LOGS/scripts.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)