import os
from scripts.logging_config import logger

def save_file(folder_name:str,file_name:str,content:str):
    """
    Saves a file in the specified folder.
    """
    logger.info(f"Saving file {file_name} in {folder_name}")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    file_path = os.path.join(folder_name,file_name)

    with open(file_path,"w") as new_file:
        new_file.write(content)
    logger.info(f"File saved successfully at {file_path}")
    