"""
Flask settings, and other custom settings specific to the driver.
"""
import os
# Flask Configuration
# ---------------------------------------------------------------
# NOTE: These three settings are only set in the app via runserver (local development)
#       If you want to use the HOST and PORT in prod, you need to access it in the gunicorn script
FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT = os.environ.get('FLASK_PORT', 8000)
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)

# Email Settings
# -----------------------------------------
RECIPIENT_LIST = (
    'contact@markliederbach.com',
)
ERROR_RECIPIENT_LIST = RECIPIENT_LIST


#  Client Settings
# -----------------------------------------
CLIENT_SETTINGS = {
    'launch_library': {
        'base_url': os.environ.get('LAUNCH_LIBRARY_BASE_URL'),
        'username': os.environ.get('LAUNCH_LIBRARY_USERNAME', default=None),
        'password': os.environ.get('LAUNCH_LIBRARY_PASSWORD', default=None),
        'timeout': os.environ.get('LAUNCH_LIBRARY_TIMEOUT', default=10),
        'verify': os.environ.get('LAUNCH_LIBRARY_VERIFY', default=True),
        'launch_endpoint': os.environ.get('LAUNCH_LIBRARY_LAUNCH_ENDPOINT', default="/launch/"),
    }
}

#  Import Logging Settings
# -----------------------------------------
from .logging_settings import *

# DEPLOYMENT INFORMATION
# ------------------------------------------------------------------------------
DEPLOYED_ENVIRONMENT = os.environ.get('DEPLOYED_ENVIRONMENT', default=None)
BUILD_STABILITY = os.environ.get('BUILD_STABILITY', default=None)
BUILD_VERSION = os.environ.get('BUILD_VERSION', default=None)
BUILD_TIMESTAMP = os.environ.get('BUILD_TIMESTAMP', default=None)
BUILD_APP_UUID = os.environ.get('BUILD_APP_UUID', default=None)
