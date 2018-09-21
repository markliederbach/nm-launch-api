"""This is where all Flask blueprints are registered with the central app."""
__version__ = "0.0.1"

import os
from flask import Flask
from nm_launch_api.api.v1 import api as api_v1
#from nm_launch_api.utils.jobs import PrimaryFlaskWorker

app = Flask(__name__)

# Get location of settings file to use
nm_launch_api_settings = os.environ.get(
    'NM_LAUNCH_API_SETTINGS',  # Environment variable
    'nm_launch_api.config.production'  # Default settings file to use
)

# Load settings file
app.config.from_object(nm_launch_api_settings)
app.logger.info("nm_launch_api is initializing")
app.logger.debug("nm_launch_api is using settings: {}".format(
    nm_launch_api_settings
))

# Here you can initialize any other components of your app.
# For example, a scheduler. You can even attach the object to the app instance.
# . . .

# Register API blueprints
app.register_blueprint(api_v1, url_prefix='/api/v1')

# Load any remaining top-level views not under API versioning
import nm_launch_api.views
