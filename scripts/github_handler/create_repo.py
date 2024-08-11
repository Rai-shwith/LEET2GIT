from github import Github

def create_repo(user,repo_name:str,description:str="",private:bool=True):
    repo = user.create_repo(repo_name,description=description,private=private)
    return repo

