from flask import current_app
from nm_launch_api.clients.launch_library.http import LaunchLibraryClient


def get_client_mapping():
    """
    Provide a dictionary mapping a key to a client
    Returns:
        dict: mapping of provider key to client class
    """
    return {
        'launch_library': LaunchLibraryClient,
    }


def get_client(provider):
    """
    Instantiated client class from the given provider
    Args:
        provider (str): Key to the above client mapping
    Returns:
        Client(BaseMappingClient): A subclassed (BaseMappingClient) client object
    """
    return get_client_mapping()[provider](**current_app.config['CLIENT_SETTINGS'][provider])
