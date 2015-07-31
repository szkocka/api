from datetime import datetime
from flask.ext.restful import Resource
from flask import request
from common.util import handle_object_id


class Researches(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def post(self, current_user):
        def add_research():
            json = request.json

            research_id = self.researches.insert_one({
                'supervisor': current_user.id(),
                'created': datetime.now(),
                'title': json['title'],
                'tags': json['tags'],
                'area': json['area'],
                'description': {
                    'brief': json['description']['brief'],
                    'detailed': json['description']['detailed']
                },
                'researchers': []
            }).inserted_id

            return {'research_id': str(research_id)}, 201

        return add_research()

    def get(self):
        def list_researches():
            researches = self.researches.find()
            return map(handle_object_id, researches), 200

        return list_researches()
