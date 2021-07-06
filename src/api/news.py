from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from src import db
from src.api.models import News

news_blueprint = Blueprint("news", __name__)
api = Api(news_blueprint)

news = api.model(
    "News",
    {
        "id": fields.Integer(readOnly=True),
        "title": fields.String(required=True),
        "url": fields.String(required=True),
        "date_added": fields.DateTime,
        "credibility": fields.Float(required=True),
    },
)


class NewsList(Resource):
    @api.expect(news, validate=True)
    def post(self):
        post_data = request.get_json()
        title = post_data.get("title")
        url = post_data.get("url")
        credibility = post_data.get("credibility")
        response_object = {}

        news = News.query.filter_by(title=title).first()

        db.session.add(News(title=title, url=url, credibility=credibility))
        db.session.commit()

        response_object["message"] = f"{title} was added!"

        return response_object, 201

    @api.marshal_with(news, as_list=True)
    def get(self):
        return News.query.all(), 200


class _News(Resource):
    @api.marshal_with(news)
    def get(self, news_id):
        news = News.query.filter_by(id=news_id).first()
        if not news:
            api.abort(404, f"News {news_id} does not exist")
        return news, 200

    def delete(self, news_id):
        response_object = {}
        news = News.query.filter_by(id=news_id).first()

        if not news:
            api.abort(404, f"News {news_id} does not exist")

        db.session.delete(news)
        db.session.commit()

        response_object["message"] = f"{news.title} was removed!"
        return response_object, 200

    @api.expect(news, validate=True)
    def put(self, news_id):
        post_data = request.get_json()
        title = post_data["title"]
        url = post_data["url"]
        credibility = post_data["credibility"]
        response_object = {}

        news = News.query.filter_by(id=news_id).first()

        if not news:
            api.abort(404, f"News {news_id} does not exist")

        news.title = title
        news.url = url
        news.credibility = credibility

        response_object["message"] = f"{news.id} was updated!"
        return response_object, 200


api.add_resource(NewsList, "/news")
api.add_resource(_News, "/news/<int:news_id>")
