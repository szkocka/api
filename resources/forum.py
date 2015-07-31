from datetime import datetime
from bson import ObjectId
from flask import request
from flask.ext.restful import Resource
from common.util import handle_object_id
from security import authenticate


class Forum(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.messages = self.db['messages']

    def get(self, forum_id):
        def get_forum():
            forum = self.forums.find_one({'_id': ObjectId(forum_id)})

            if forum is None:
                return {'message': 'Forum with ID: {0} not found.'.format(forum_id)}, 404

            messages = self.messages.find({'forum': forum_id})

            return {
                'forum': handle_object_id(forum),
                'messages': map(handle_object_id, messages)
            }, 200

        return get_forum()

    def post(self, forum_id, current_user):
        def add_message():
            json = request.json

            message_id = self.messages.insert_one({
                "createBy": current_user.id(),
                "created": datetime.now(),
                "body": json["body"],
                "forum": forum_id
            }).inserted_id

            return {"message_id": str(message_id)}, 201

        return add_message()
