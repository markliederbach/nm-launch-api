from nm_launch_api.clients.base import BaseAPIClient


class LaunchLibraryClient(BaseAPIClient):
    def __init__(self, base_url, launch_endpoint, **kwargs):
        self.launch_endpoint = launch_endpoint
        super().__init__(base_url=base_url, **kwargs)

    def get_launches(self, params):
        """
        Call the launch_endpoint with requested params.
        Args:
            params(dict): params to pass to Launch API

        Returns:
            dict: Parsed data from the remote resource.

        """
        return self.get_data(
            endpoint=self.launch_endpoint,
            params=params,
        )
