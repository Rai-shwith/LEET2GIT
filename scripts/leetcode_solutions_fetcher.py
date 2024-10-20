import requests
from fastapi import HTTPException
URL = 'https://leetcode.com/api/submissions/?offset=0&limit=4000&lastkey='

def leetcode_solution_fetcher(leetcode_access_token: str,csrftoken : str):
    cookies = {
    'LEETCODE_SESSION': leetcode_access_token,
    'csrftoken': 'ozzJoQrSgQWUzJLMsmfhV2gGXv1H6rAgTC9PyrGAyL8olNx114p4u7vyYJvCECzK'
    }
    # Make the GET request to the API endpoint with cookies
    response = requests.get(URL, cookies = cookies)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch the leetcode submissions")