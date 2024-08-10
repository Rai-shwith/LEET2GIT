import pytest
from scripts.problem_fetcher import *
from scripts.utils import *
from fastapi import HTTPException
import os

def test_url_maker():
    url = url_maker("roman to-integer/")
    assert url == "https://alfa-leetcode-api.onrender.com/select?titleSlug=roman-to-integer"


def test_get_problem_details():
    problem_details = get_problem_details("roman to-integer")
    assert isinstance(problem_details,dict)

def test_save_file():
    folder_name = "OUTPUT/1234-a-b-c"
    file_name = "test.txt"
    content = "qwertyuioplkjjasdfghjklzxcvbnm"
    save_file(folder_name=folder_name,file_name=file_name,content=content)
    assert os.path.exists(f"{folder_name}/{file_name}")
    os.remove(f"{folder_name}/{file_name}")
    os.rmdir(folder_name)
