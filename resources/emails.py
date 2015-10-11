from flask import request
from flask.ext.restful import Resource

from app import db
from common.http_responses import ok_msg
from common.insert_wraps import insert_research
from common.validation import validate_request
from common.security import authenticate, is_supervisor
from mailer.mailer import Mailer
from mailer.views import InviteToJoinSubj, InviteToJoin, ReqToJoinSubj, ReqToJoin

mailer = Mailer()


class InviteToJoinResearch(Resource):
    method_decorators = [is_supervisor, insert_research, validate_request, authenticate]
    required_fields = ['email']  # used by validate_request

    def post(self, research, current_user):
        email, text = self.__request_fields()

        self.__send_invite(current_user, email, research, text)

        research.researchers.append(email)
        research.researchers = list(set(research['researchers']))

        db.update()
        return ok_msg("Invitation send to {0}".format(email))

    def __request_fields(self):
        json = request.json
        return json['email'], json.get('text', '')

    def __send_invite(self, current_user, email, research, text):
        supervisor = current_user.name
        title = research['title']
        description = research.brief_desc
        user = db.find_user_by_email(email)
        researcher = user.name if user else email

        mailer.send(
            InviteToJoinSubj(supervisor, title),
            InviteToJoin(supervisor, title, description, researcher, text), [email])


class ReqToJoinResearch(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, research, current_user):
        text = request.json.get('text', '')
        title = research['title']
        supervisor = research.supervisor
        user_name = current_user.name

        mailer.send(
            ReqToJoinSubj(user_name, title),
            ReqToJoin(supervisor.name, user_name, title, text), [supervisor.email])

        return ok_msg('Request to join was send to {0}'.format(supervisor.email))
