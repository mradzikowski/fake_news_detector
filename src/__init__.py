from flask import Flask, jsonify
from flask_restx import Resource, Api
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

api = Api(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    broadcaster = db.Column(db.String(128), nullable=True)
    url = db.Column(db.String(128), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    credibility = db.Column(db.Float, default=0, nullable=False)

    def __init__(self, title, credibility):
        self.title = title
        self.credibility = credibility


class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(Ping, '/ping')