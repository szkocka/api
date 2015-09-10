from datetime import datetime

from flask import request
from flask.ext.restful import Resource
from common.http_responses import ok, created
from common.insert_wraps import insert_research
from common.validation import validate_request
from common.prettify_responses import prettify_researches, prettify_research
from common.security import authenticate, is_supervisor


class ListResearches(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']

    def get(self):
        researches = self.researches.find()

        return ok(
            {
                'researches': prettify_researches(self.users, researches)
            }
        )


class GetResearch(Resource):
    method_decorators = [insert_research]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']

    def get(self, research):
        return ok(prettify_research(self.users, research))


class AddResearch(Resource):
    method_decorators = [validate_request, authenticate]
    required_fields = ['title', 'area', 'description']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def post(self, current_user):
        research = self.__create(current_user, request.json)
        research_id = self.__save(research)

        return created(
            {
                'research_id': str(research_id)
            }
        )

    def __save(self, research):
        return self.researches.insert_one(research).inserted_id

    def __create(self, current_user, json):
        description = json['description']

        return {
            'supervisor': current_user.id(),
            'created': datetime.now(),
            'title': json['title'],
            'tags': json.get('tags', []),
            'area': json['area'],
            'status': 'active',
            'description': {
                'brief': description.get('brief', ''),
                'detailed': description.get('detailed', '')
            },
            'researchers': [],
            'image_url': json.get('image_url', None)
        }

class UpdateResearch(Resource):
    method_decorators = [is_supervisor, insert_research, authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def put(self, research, current_user):
        json = request.json

        research['title'] = json.get('title', research['title'])
        research['tags'] = json.get('tags', research['tags'])
        research['area'] = json.get('area', research['area'])
        research['status'] = json.get('status', research['status'])
        research['image_url'] = json.get('image_url', research['image_url'])
        research['description'] = json.get('description', research['description'])

        research_id = self.__save(research)

        return ok(
            {
                'research_id': str(research_id)
            }
        )

    def __save(self, research):
        return self.researches.save(research)
