from datetime import datetime
from flask import request
from flask.ext.restful import Resource
from common.util import handle_object_id
from security import authenticate


class Forums(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']

    def get(self, research_id):
        def list_forums():
            forums = self.forums.find({"research": research_id})
            return map(handle_object_id, forums), 200

        return list_forums()

    def post(self, research_id, current_user):
        def add_forum():
            json = request.json

            forum_id = self.forums.insert_one({
                "createBy": current_user.id(),
                "created": datetime.now(),
                "subject": json["subject"],
                "research": research_id
            }).inserted_id

            return {"forum_id": str(forum_id)}, 201

        return add_forum()
