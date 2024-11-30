import logging
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s',
                    handlers=[logging.FileHandler("LOGS/scripts.log","a"), logging.StreamHandler()])
logger = logging.getLogger(__name__)