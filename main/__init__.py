from flask import Flask, request
from flask_cors import CORS
import re

def _after_request(response):
    allowed_origins = [
        re.compile('https?://(.*\.)?localhost')
    ]

    origin = request.headers.get('Origin')
    if origin:
        for allowed_origin in allowed_origins:
            if allowed_origin.match(origin):
                response.headers['Access-Control-Allow-Origin'] = origin

    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'

    return response

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
    app.after_request(_after_request)
    load_app_config(app)
    register_error_handler(app)
    api.init_app(app)
    models.init_app(app)
    CORS(app)
    return app