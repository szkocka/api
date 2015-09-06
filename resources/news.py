from datetime import datetime

from flask import request
from flask.ext.restful import Resource
from common.http_responses import ok, created

from common.validation import validate_request
from common.prettify_responses import prettify_news
from common.security import authenticate


class ListNews(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.news = self.db['news']
        self.users = self.db['users']
        self.logger = kwargs['logger']

    def get(self):
        news = self.__find_news()

        return ok(
            {
                'news': prettify_news(self.users, news)
            }
        )

    def __find_news(self):
        return self.news.find().sort('created')


class AddNews(Resource):
    method_decorators = [authenticate, validate_request]
    required_fields = ['title', 'body']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.news = self.db['news']
        self.logger = kwargs['logger']

    def post(self, current_user):
        title, body = self.__request_fields()
        new_news = self.__create(current_user, title, body)
        news_id = self.__save(new_news)

        return created(
            {
                'news_id': str(news_id)
            }
        )

    def __save(self, new_news):
        return self.news.insert_one(new_news).inserted_id

    def __create(self, current_user, title, body):
        return {
            "createdBy": current_user.id(),
            "created": datetime.now(),
            "title": title,
            "body": body
        }

    def __request_fields(self):
        json = request.json
        return json["title"], json["body"]
