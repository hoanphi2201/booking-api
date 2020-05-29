from flask import Flask
from flask_cors import CORS

def create_app():
    import config
    import os
    from . import models
    from .apis import api
    from .extensions.error_handlers import register_error_handler

    def load_app_config(app):
        app.config.from_object(config)
        app.config.from_pyfile('config.py', silent=True)

    app = Flask(__name__)
    load_app_config(app)
    register_error_handler(app)
    api.init_app(app)
    models.init_app(app)
    CORS(app)
    return app