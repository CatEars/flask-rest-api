import os

from flask import Flask
from dynaconf import FlaskDynaconf

from .routes import create_routes
from .db import initialize_db
from .cache import initialize_cache
from .tasks import initialize_tasks


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    FlaskDynaconf(app, settings_file=['settings.toml'])

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    initialize_db(app)
    initialize_cache(app)
    initialize_tasks(app)
    create_routes(app)

    return app
