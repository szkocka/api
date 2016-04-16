import os

from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok, created
from common.security import authenticate, is_admin
from common.validation import validate_request
from model.db import News
from model.resp import NewsListJson


class ListNews(Resource):
    def get(self):
        return ok(NewsListJson(News.all()).to_json())


class AddNews(Resource):
    method_decorators = [is_admin, validate_request, authenticate]
    required_fields = ['title', 'body']  # used by validate_request

    def post(self, current_user):
        title = request.json['title']
        body = request.json['body']

        default_image_url = os.environ['DEFAULT_IMAGE']
        image_url = request.json.get('image_url', default_image_url)

        news = News(creator_key=current_user.key,
                    title=title,
                    body=body,
                    image_url=image_url)

        return created(
            {
                'news_id': news.put().id()
            }
        )
