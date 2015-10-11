from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok, created
from common.validation import validate_request
from common.prettify_responses import prettify_news
from common.security import authenticate
from db.model import News
from db.repository import save


class ListNews(Resource):
    def get(self):
        return ok(
            {
                'news': prettify_news(db.all_news())
            }
        )


class AddNews(Resource):
    method_decorators = [validate_request, authenticate]
    required_fields = ['title', 'body']  # used by validate_request

    def post(self, current_user):
        title = request.json["title"]
        body = request.json["body"]

        news = News(current_user, title, body)

        save(news)
        return created(
            {
                'news_id': news.id
            }
        )
