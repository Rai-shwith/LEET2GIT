import requests
from fastapi import HTTPException
BASE_URL = 'https://leetcode.com/api/submissions/'

def leetcode_solution_fetcher(leetcode_access_token: str,csrftoken : str):
    submissions = {"submissions_dump": []}
    # Leetcode provides the solution in small chunks of 20, So this function uses while loop
    cookies = {
    'LEETCODE_SESSION': leetcode_access_token,
    'csrftoken': 'ozzJoQrSgQWUzJLMsmfhV2gGXv1H6rAgTC9PyrGAyL8olNx114p4u7vyYJvCECzK'
    }
    last_key = "" # This is the key that will be used to fetch the next 20 solutions
    while True:
        # Make the GET request to the API endpoint with cookies
        response = requests.get(f'{BASE_URL}?lastkey={last_key}', cookies = cookies)
        data = response.json()
        # Check if the response is successful
        if response.status_code == 200:
            # Append the fetched submissions to the submissions list
            submissions["submissions_dump"].extend(data.get('submissions_dump', []))
            last_key = data['last_key']
            # check the end of submissions
            if data["has_next"] == False:
                break
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch the leetcode submissions")
    return submissions