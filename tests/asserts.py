import os
import json
from tests.mock_clients.mock_response import MockResponse

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_DIRECTORY_PATH = os.path.join(TEST_DIR, 'expected_responses')


class BaseViewsAssert:

    def __init__(self, test_case, request, response, query_mock_method, test_profile, run_assertions=True, **kwargs):
        self.test = test_case
        self.request = request
        self.response, self.status_code = response
        self.query_mock_method = query_mock_method
        self.test_profile = test_profile
        self.extra_options = kwargs
        if run_assertions:
            self.assertions()

    def assert_response_status(self, code):
        """Extracted method to assert a response code."""
        self.test.assertEqual(self.status_code, code)

    def assert_okay_status(self):
        """Response code is 200."""
        self.assert_response_status(200)

    def assert_json_data(self, expected_data):
        self.test.assertDictEqual(json.loads(self.response.data), expected_data)

    def assert_response_matches_expected(self, payload_profile):
        expected_response = self._load_expected_response(payload_profile)
        self.assert_response_status(expected_response.status_code)
        self.assert_json_data(expected_response.json())

    def assertions(self):
        self.test.assertTrue(self.query_mock_method.called)
        self.assert_okay_status()

    @staticmethod
    def _load_expected_response(payload_profile):
        with open(os.path.join(JSON_DIRECTORY_PATH, '{}.json'.format(payload_profile)), 'r') as f:
            return MockResponse(**json.load(f))


class LaunchScheduleAssert(BaseViewsAssert):

    def assertions(self):
        super().assertions()
        self.assert_response_matches_expected(self.test_profile)
