from nm_launch_api.clients.base import BaseAPIClient


class LaunchLibraryClient(BaseAPIClient):
    def __init__(self, base_url, launch_endpoint, **kwargs):
        self.launch_endpoint = launch_endpoint
        super().__init__(base_url=base_url, **kwargs)

    def get_launches(self, params, search_term=None):
        """
        Call the launch_endpoint with requested params.
        Args:
            params(dict): params to pass to Launch API
            search_term(str): optional search term to filter results with

        Returns:
            dict: Parsed data from the remote resource.

        """
        endpoint = "/".join([self.launch_endpoint, search_term if search_term else ""])
        return self.get_data(
            endpoint=endpoint,
            params=params,
        )
