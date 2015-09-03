from datetime import datetime

from bson import ObjectId
from flask import request
from flask.ext.restful import Resource

from common.util import is_supervisor
from mailer.views import InviteToJoinSubj, InviteToJoin
from common.prettify_responses import prettify_researches, prettify_research
from security.authenticate import authenticate


class GetResearch(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']

    def get(self, research_id):
        research = self.researches.find_one({'_id': ObjectId(research_id)})

        if research is None:
            return {'message': 'Research with ID: {0} not found.'.format(research_id)}, 404

        return prettify_research(self.users, research), 200


class UpdateResearch(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def put(self, research_id, current_user):
        json = request.json

        research = self.researches.find_one({'_id': ObjectId(research_id)})

        if research is None:
            return {'message': 'Research with ID: {0} not found.'.format(research_id)}, 404

        if not is_supervisor(current_user, research):
            return {'message': 'You must be supervisor to update research.'}, 403

        research['title'] = json['title']
        research['tags'] = json['tags']
        research['area'] = json['area']
        research['status'] = json['status']
        research['image_url'] = json['image_url']
        research['description'] = {
            'brief': json['description']['brief'],
            'detailed': json['description']['detailed']
        }

        research_id = self.researches.save(research)

        return {'research_id': str(research_id)}, 200


class AddResearch(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def post(self, current_user):
        json = request.json

        insert = self.researches.insert_one(
            self.new_research(current_user, json))

        return {'research_id': str(insert.inserted_id)}, 201

    def new_research(self, current_user, json):
        return {
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
            'researchers': [],
            'image_url': json['image_url']
        }


class ListResearches(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']

    def get(self):
        researches = self.researches.find()
        return {'researches': prettify_researches(self.users, researches)}, 200


class InviteToJoinResearch(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']
        self.mailer = kwargs['mailer']

    def post(self, research_id, current_user):
        research = self.researches.find_one({'_id': ObjectId(research_id)})

        if research is None:
            return {'message': 'Research with ID: {0} not found.'.format(research_id)}, 404

        if not is_supervisor(current_user, research):
            return {'message': 'You must be supervisor for inviting to join research.'}, 403

        json = request.json
        email = json['email']

        #self.send_invite(current_user, email, research, json['text'])
        self.update_research(email, research)

        return {'message': "Invitation send to {0}".format(email)}, 200

    def send_invite(self, current_user, email, research, text):
        supervisor = current_user.user['name']
        title = research['title']
        description = research['description']['brief']
        researcher = self.researcher_name(email)

        self.mailer.send(
            InviteToJoinSubj(supervisor, title),
            InviteToJoin(supervisor, title, description, researcher, text), [email])

    def update_research(self, email, research):
        research['researchers'].append(email)
        research['researchers'] = list(set(research['researchers']))
        self.researches.save(research)

    def researcher_name(self, email):
        user = self.users.find_one({'email': email})

        if user is None:
            return email
        else:
            return user['name']


class ReqToJoinResearch(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']
        self.mailer = kwargs['mailer']

    def post(self, research_id, current_user):
        research = self.researches.find_one({'_id': ObjectId(research_id)})

        if research is None:
            return {'message': 'Research with ID: {0} not found.'.format(research_id)}, 404

        json = request.json

        text = json['text']

        supervisor = self.supervisor_name(research)
        supervisor_name = supervisor['name']
        supervisor_email = supervisor['email']
        title = research['title']
        user = current_user.user['name']

        #self.mailer.send(
            #ReqToJoinSubj(user, title),
            #ReqToJoin(supervisor_name, user, title, text), [supervisor_email])

        return {'message': "Request to join was send to {0}".format(supervisor_email)}, 200

    def supervisor_name(self, research):
        supervisor_id = research['supervisor']
        return self.users.find_one({'_id': ObjectId(supervisor_id)})

