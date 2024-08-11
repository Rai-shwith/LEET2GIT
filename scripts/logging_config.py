import logging
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(funcname)s-%(message)s',
                    handlers=[logging.FileHandler("scripts.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)