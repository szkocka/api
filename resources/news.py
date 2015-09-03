from datetime import datetime

from flask import request
from flask.ext.restful import Resource
from common.validation import validate_request
from resources.prettify_responses import prettify_news

from security.authenticate import authenticate


class ListNews(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.news = self.db['news']
        self.users = self.db['users']
        self.logger = kwargs['logger']

    def get(self, current_user):
        news = self.news.find().sort('created')
        return {'news': prettify_news(self.users, news)}, 200


class AddNews(Resource):
    method_decorators = [authenticate, validate_request]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.news = self.db['news']
        self.logger = kwargs['logger']
        self.required_fields = ['title', 'body']

    def post(self, current_user):
        title, body = self.__fields(request.json)
        new_news = self.__create(current_user, title, body)
        news_id = self.__save(new_news)

        return {'news_id': str(news_id)}, 201

    def __save(self, new_news):
        return self.news.insert_one(new_news).inserted_id

    def __create(self, current_user, title, body):
        return {
            "createdBy": current_user.id(),
            "created": datetime.now(),
            "title": title,
            "body": body
        }

    def __fields(self, json):
        return json["title"], json["body"]
