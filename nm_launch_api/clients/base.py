import os
import pprint
import certifi
import requests
import threading
from flask import current_app
from nm_launch_api import exceptions


class BaseAPIClient:

    requests = requests
    certifi = certifi
    certifi.where()

    def __init__(
            self,
            base_url,
            username=None,
            password=None,
            timeout=10,
            verify=True,
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.verify = verify
        self.threaded_session = {}

    def __str__(self):
        return "[{}: {}]".format(self.__class__.__name__, self.base_url)

    def __enter__(self):
        """For use as a context statement. You can simply say:
        with self as session:
            session.get(...)

        This will open and provide a session to use for requests,
        then close it when complete, using __exit__."""
        self.threaded_session[threading.currentThread().ident] = self.get_session()
        return self.threaded_session[threading.currentThread().ident]

    def __exit__(self, *exc):
        """Used to close context statement."""
        self.threaded_session[threading.currentThread().ident].close()
        self.threaded_session[threading.currentThread().ident] = None
        return False

    def get_session(self):
        """Configure a requests session to use."""
        sess = self.requests.Session()
        sess.trust_env = False
        sess.verify = (
            os.environ.get(
                "REQUESTS_CA_BUNDLE", default=self.certifi.where()
            )
            if self.verify is True
            else self.verify
        )
        if self.username and self.password:
            sess.auth = (self.username, self.password)
        return sess

    def get_client_exception_class(self):
        return exceptions.ClientException

    def get_data(self, endpoint, raw=False, params=None):
        """
        Higher-level GET method, which returns only the JSON data
        Args:
            endpoint (str): Resource to request
            raw (bool): True if it is desired to skip JSON parsing
            params (dict): key/values to be parsed as query parameters
        Returns:
            dict: JSON data OR
            Response: if raw is true
        """
        current_app.logger.debug(
            "Sending GET request to {} with params:\n{}".format(
                endpoint, pprint.pformat(params, indent=2)
            )
        )
        response = self._get_data_for_request(endpoint=endpoint, params=params)
        json_data = self.parse_query_data(response)
        current_app.logger.debug(
            "Response JSON from {}:\n{}".format(
                endpoint, pprint.pformat(json_data, indent=2, depth=1)
            )
        )
        return response if raw else json_data

    def _get_data_for_request(self, endpoint, params=None):
        """
        Low-level GET method, with mild error handling.
        Args:
            endpoint (str): Resource to request
            params (dict): key/values to be parsed as query parameters

        Returns:
            Response: Raw response from remote resource
        """
        response = None
        try:
            with self as session:
                response = session.get(
                    "{}{}".format(self.base_url, endpoint),
                    timeout=self.timeout,
                    params=params if params is not None else {},
                )
        except self.requests.exceptions.RequestException as e:
            raise self.get_client_exception_class()(
                str(e), self.requests.codes["service_unavailable"]
            )
        except Exception as e:
            raise self.get_client_exception_class()(
                str(e), self.requests.codes["bad_request"]
            )
        if not (200 >= response.status_code < 300):
            raise self.get_client_exception_class()(
                self.get_reason(response), response.status_code
            )
        return response

    @staticmethod
    def parse_query_data(response):
        """
        Extracted method to parse response from request.
        If response is in json, it will return a python dict, else raw text.

        Args:
            response (object): requests.Response

        Returns:
            : either the json or the data it failed on
        """
        if response.headers.get("content-type") == "application/json":
            return response.json()
        return response.text

    @staticmethod
    def get_reason(response):
        """
        Get's the reason for not returning a 2** code

        Args:
            response (object): response payload

        Returns:
            string: the payload detail key value
        """
        result = "Reason: {} {}".format(response.status_code, response.reason)
        if response.headers.get("content-type") == "application/json":
            response_data = response.json()
            if response_data:
                if "detail" in response_data:
                    result += ", Detail: {}".format(response_data["detail"])
                elif "message" in response_data:
                    result += ", Detail: {}".format(response_data["message"])
                elif "error" in response_data:
                    result += ", Detail: {}".format(response_data["error"])
                else:
                    result = response_data
        else:
            response_data = response.text
            result += ", Detail: {}".format(pprint.pformat(response_data, indent=2))

        if isinstance(result, (list)):
            result = " ".join(result)
        return result.replace('"', "").replace("'", "")
