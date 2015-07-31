from datetime import datetime
from flask import request
from flask.ext.restful import Resource
from common.util import handle_object_id
from security import authenticate


class News(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.news = self.db["news"]
        self.logger = kwargs['logger']

    def post(self, current_user):
        def add_news():
            json = request.json

            news_id = self.news.insert_one({
                "createBy": current_user.id(),
                "created": datetime.now(),
                "title": json["title"],
                "body": json["body"]
            }).inserted_id

            return {news_id: str(news_id)}, 201

        return add_news()

    def get(self):
        def list_news():
            return map(handle_object_id, self.news.find())

        return list_news()
