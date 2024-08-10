import os

def save_file(folder_name:str,file_name:str,content:str):
    """
    Saves a file in the specified folder.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    file_path = os.path.join(folder_name,file_name)

    with open(file_path,"w") as new_file:
        new_file.write(content)
    