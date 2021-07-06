from flask import Flask, jsonify
from flask_restx import Resource, Api
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



db = SQLAlchemy()

def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from src.api.ping import ping_blueprint
    app.register_blueprint(ping_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
