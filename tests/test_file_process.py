from unittest.mock import patch
import pytest
import os
from fastapi import HTTPException
from scripts.problem_fetcher import *
from scripts.utils import *
from scripts.create_problem_files import solution_file_creater

# @pytest.fixture
# def mock_save_file():
#     with patch('scripts.problem_fetcher.save_file') as mock:
#         yield mock

def test_url_maker():
    url = url_maker("roman to-integer/")
    assert url == "https://alfa-leetcode-api.onrender.com/select?titleSlug=roman-to-integer"

def test_get_problem_details():
    problem_details = get_problem_details("roman to-integer")
    assert isinstance(problem_details, dict)

def test_save_file():
    folder_name = "OUTPUT/1234-a-b-c"
    file_name = "test.txt"
    content = "qwertyuioplkjjasdfghjklzxcvbnm"
    save_file(folder_name=folder_name, file_name=file_name, content=content)
    assert os.path.exists(os.path.join(folder_name, file_name))
    os.remove(os.path.join(folder_name, file_name))
    os.rmdir(folder_name)



# def test_solution_file_creater(mock_save_file):
#     # Test inputs
#     solution = {
#         'question_id': 1234,
#         'title_slug': 'example-problem',
#         'code': 'print("Hello, world!")'
#     }
#     code_extension = '.py'

#     # Expected outputs
#     expected_folder_name = 'OUTPUT/1234-example-problem'
#     expected_file_name = 'Solution.py'
#     expected_content = 'print("Hello, world!")'

#     # Call the function
#     solution_file_creater(solution, code_extension)

#     # Assert that save_file was called with the correct arguments
#     mock_save_file.assert_called_once_with(
#         folder_name=expected_folder_name,
#         file_name=expected_file_name,
#         content=expected_content
#     )
#     # Clean up the created file and folder
#     if os.path.exists(os.path.join(expected_folder_name, expected_file_name)):
#         os.remove(os.path.join(expected_folder_name, expected_file_name))
#     if os.path.exists(expected_folder_name):
#         os.rmdir(expected_folder_name)
