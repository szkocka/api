from bson import ObjectId
from flask import request
from flask.ext.restful import Resource
from common.http_responses import ok_msg
from common.insert_wraps import insert_research
from common.validation import validate_request
from mailer.views import InviteToJoinSubj, InviteToJoin, ReqToJoinSubj, ReqToJoin
from common.security import authenticate, is_supervisor


class InviteToJoinResearch(Resource):
    method_decorators = [authenticate, validate_request, insert_research, is_supervisor]
    required_fields = ['email', 'text']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']
        self.mailer = kwargs['mailer']

    def post(self, research, current_user):
        email, text = self.__request_fields()

        self.__send_invite(current_user, email, research, text)
        self.__update_research(email, research)

        return ok_msg("Invitation send to {0}".format(email))

    def __request_fields(self):
        json = request.json
        return json['email'], json['text']

    def __send_invite(self, current_user, email, research, text):
        supervisor = current_user.name()
        title = research['title']
        description = research['description']['brief']
        researcher = self.__researcher_name(email)

        self.mailer.send(
            InviteToJoinSubj(supervisor, title),
            InviteToJoin(supervisor, title, description, researcher, text), [email])

    def __update_research(self, email, research):
        research['researchers'].append(email)
        research['researchers'] = list(set(research['researchers']))
        self.researches.save(research)

    def __researcher_name(self, email):
        user = self.users.find_one({'email': email})

        if user is None:
            return email
        else:
            return user['name']


class ReqToJoinResearch(Resource):
    method_decorators = [authenticate, validate_request, insert_research]
    required_fields = ['text']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']
        self.users = self.db['users']
        self.mailer = kwargs['mailer']

    def post(self, research, current_user):
        text = request.json['text']
        sup_name, sup_email = self.__supervisor_fields(research)
        title = research['title']
        user_name = current_user.name()

        self.mailer.send(
            ReqToJoinSubj(user_name, title),
            ReqToJoin(sup_name, user_name, title, text), [sup_email])

        return ok_msg('Request to join was send to {0}'.format(sup_email))

    def __supervisor_fields(self, research):
        supervisor = self.users.find_one(
            {
                '_id': ObjectId(research['supervisor'])
            }
        )
        return supervisor['name'], supervisor['email']
