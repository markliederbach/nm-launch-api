"""File to hook into gunicorn for production deployments."""
from nm_launch_api import app


if __name__ == '__main__':
    app.run()