from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok, created
from common.validation import validate_request
from common.prettify_responses import prettify_news
from common.security import authenticate
from model.db import News


class ListNews(Resource):
    def get(self):
        return ok(
            {
                'news': prettify_news(News.all())
            }
        )


class AddNews(Resource):
    method_decorators = [validate_request, authenticate]
    required_fields = ['title', 'body']  # used by validate_request

    def post(self, current_user):
        title = request.json["title"]
        body = request.json["body"]

        news = News(creator_key=current_user.key,
                    title=title,
                    body=body)

        return created(
            {
                'news_id': news.put().id()
            }
        )
