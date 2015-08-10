from bson import ObjectId
from datetime import datetime
from flask import request
from flask.ext.restful import Resource
from common.util import handle_object_id
from security.authenticate import authenticate

class GetResearch(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def get(self, research_id, current_user):
        research = self.researches.find_one({'_id': ObjectId(research_id)})

        if research is None:
            return {'message': 'Research with ID: {0} not found.'.format(research_id)}, 404

        return handle_object_id(research), 200


class UpdateResearch(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def put(self, research_id, current_user):
        return research_id


class AddResearch(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def post(self, current_user):
        json = request.json

        research_id = self.researches.insert_one({
            'supervisor': current_user.id(),
            'created': datetime.now(),
            'title': json['title'],
            'tags': json['tags'],
            'area': json['area'],
            'status': 'active',
            'description': {
                'brief': json['description']['brief'],
                'detailed': json['description']['detailed']
            },
            'researchers': []
        }).inserted_id

        return {'research_id': str(research_id)}, 201


class ListResearches(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def get(self):
        researches = self.researches.find()
        return {'researches': map(handle_object_id, researches)}, 200