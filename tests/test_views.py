"""
Tests for the nm_launch_api module.
"""

import os
import json
import unittest
from unittest import mock
import collections
from nm_launch_api import app
from nm_launch_api.api.v1 import views as v1_views
from tests.mock_clients import launch_library


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_DIRECTORY_PATH = os.path.join(TEST_DIR, "mock_requests")


class TestNMLaunchAPIV1(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.view = v1_views.LaunchSchedule()

    @mock.patch('nm_launch_api.clients.base.BaseAPIClient._get_data_for_request',
                side_effect=launch_library.mock_launch_library_get_data_for_request)
    def wrapped_request(self, test_profile, query_mock_method, **kwargs):
        request, response = self.submit_request('{}.json'.format(test_profile), **kwargs)
        return query_mock_method, request, response

    @staticmethod
    def build_request_args(json_filename):
        MockRequest = collections.namedtuple("MockRequest", ["args"])
        with open(os.path.join(JSON_DIRECTORY_PATH, json_filename), "r") as f:
            return MockRequest(json.load(f))

    def submit_request(self, request_filename, view=None, **kwargs):
        view = view if view is not None else self.view
        request_args = self.build_request_args(request_filename)
        with self.app.test_request_context() as context:
            context.request.args = request_args
            return request_args, view.get()

    def test_000_launch_schedule(self):
        test_profile = "launch_schedule_normal"
        self.app.config["CLIENT_SETTINGS"]["launch_library"]["base_url"] = test_profile
        query_mock_method, request, response = self.wrapped_request(test_profile)



if __name__ == "__main__":
    import sys
    sys.exit(unittest.main())
