import os
import json
from nm_launch_api import app
from tests.mock_clients.mock_response import MockResponse


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_DIRECTORY_PATH = os.path.join(TEST_DIR, 'responses')


def get_mock_response(test_profile):
    filepath = os.path.join(JSON_DIRECTORY_PATH, "{}.json".format(test_profile))
    with open(filepath, 'r') as data:
        response_data = json.load(data)
    return MockResponse(**response_data)


def mock_launch_library_get_data_for_request(*args, **kwargs):
    test_profile = app.config["CLIENT_SETTINGS"]["launch_library"]['base_url']
    return get_mock_response(test_profile)
