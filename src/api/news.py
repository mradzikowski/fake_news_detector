from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import News


news_blueprint = Blueprint('news', __name__)
api = Api(news_blueprint)

news = api.model('News', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True),
    'url': fields.String(required=True),
    'date_added': fields.DateTime,
    'credibility': fields.Float(required=True),
})


class NewsList(Resource):

    @api.expect(news, validate=True)
    def post(self):
        post_data = request.get_json()
        title = post_data.get('title')
        url = post_data.get('url')
        credibility = post_data.get('credibility')
        response_object = {}

        news = News.query.filter_by(title=title).first()
        if news:
            response_object['message'] = 'Sorry. That title already exists.'
            return response_object, 400

        db.session.add(News(title=title, url=url, credibility=credibility))
        db.session.commit()

        response_object['message'] = f'{title} was added!'

        return response_object, 201


api.add_resource(NewsList, '/news')