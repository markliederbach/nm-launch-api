import flask
from flask import current_app, request, views
from nm_launch_api import exceptions
from nm_launch_api.clients import get_client
from nm_launch_api.api.v1 import api, schemas


class LaunchSchedule(views.MethodView):
    """
    This class controls the API for sending config update requests down to collectors.
    """

    def get(self):
        """
        Return results from remote API for launch events.
        Returns:
            dict: Data to be formatted as JSON
            int: Status code for the response.
        """
        launch_client = get_client("launch_library")
        params = request.args
        current_app.logger.info("Processing {} GET request with params: {}".format(self.__class__.__name__, params))
        try:
            response_data = launch_client.get_launches(params=params)
            current_app.logger.info("Returning {} successful response".format(self.__class__.__name__))
            return flask.jsonify(self.parse_search_response(response_data)), launch_client.requests.codes['ok']
        except exceptions.ClientException as exc:
            current_app.logger.exception("View {} failed to complete request".format(self.__class__.__name__))
            return flask.jsonify({"error": str(exc)}), exc.status_code
        except Exception as exc:
            current_app.logger.exception("View {} failed to complete request".format(self.__class__.__name__))
            return flask.jsonify({"error": str(exc)}), launch_client.requests.codes['internal_server_error']

    def parse_search_response(self, raw_data):
        """
        Use ModelSchemas to format and parse the data.
        Args:
            raw_data(dict): Raw data from remote resource

        Returns:
            dict: Parsed data to be returned to the client

        """
        response_schema = schemas.LaunchInfoSchema(many=True)
        parsed_data = response_schema.dump(raw_data['launches'])
        assert not parsed_data.errors
        raw_data['launches'] = parsed_data.data
        return raw_data


api.add_url_rule('/launch', view_func=LaunchSchedule.as_view('launch'))
