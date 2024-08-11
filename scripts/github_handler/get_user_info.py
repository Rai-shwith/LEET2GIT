from github import Github

def get_user_info(access_token):
    g = Github(access_token)
    user = g.get_user()
    return user