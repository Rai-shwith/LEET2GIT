import requests
from fastapi import HTTPException
from scripts.logging_config import logger

BASE_URL = 'https://leetcode.com/api/submissions/'

def leetcode_solution_fetcher(leetcode_access_token: str):
    submissions = {"submissions_dump": []}
    # Leetcode provides the solution in small chunks of 20, So this function uses while loop
    cookies = {
    'LEETCODE_SESSION': str(leetcode_access_token),
      'Secure': 'true'
    }
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://leetcode.com',
}
    
    last_key = "" # This is the key that will be used to fetch the next 20 solutions
    while True:
        # Make the GET request to the API endpoint with cookies
        response = requests.get(f'{BASE_URL}?lastkey={last_key}', cookies = cookies, headers=headers)
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
            logger.error(response.json())
            logger.info("Failed to fetch the leetcode submissions")
            raise HTTPException(status_code=401, detail="Failed to fetch the leetcode submissions. Incorrect credentials")
    return submissions