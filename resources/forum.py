import datetime
from flask import request
from flask.ext.restful import Resource
from security import authenticate


class Forum(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.messages = self.db.messages

    def get(self, forum_id):
        pass

    def post(self, forum_id, current_user):
        def add_message():
            json = request.json

            message_id = self.messages.insert_one({
                "createBy": current_user.id(),
                "created": datetime.datetime.now(),
                "body": json["body"],
                "forum": forum_id
            }).inserted_id

            return {"message_id": str(message_id)}, 201

        return add_message()
