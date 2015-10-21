from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok_msg
from common.insert_wraps import insert_research
from common.validation import validate_request
from common.security import authenticate, is_supervisor
from db.model import InvitedResearcher
from db.repository import find_user_by_email, update, save
from mailer.mailer import Mailer
from mailer.views import InviteToJoinSubj, InviteToJoin, ReqToJoinSubj, ReqToJoin

mailer = Mailer()


class InviteToJoinResearch(Resource):
    method_decorators = [is_supervisor, insert_research, validate_request, authenticate]
    required_fields = ['email']  # used by validate_request

    def post(self, research, current_user):
        email = request.json['email']
        text = request.json.get('text', '')
        supervisor = current_user.name

        user = find_user_by_email(email)
        if user:
            research.researchers.append(user)
            update()
            researcher = user.name
        else:
            save(InvitedResearcher(user, email))
            researcher = email

        self.__send_invite(supervisor, researcher, email, research, text)

        return ok_msg("Invitation send to {0}".format(email))

    def __send_invite(self, supervisor, researcher, email, research, text):
        title = research.title
        description = research.brief_desc

        mailer.send(
            InviteToJoinSubj(supervisor, title),
            InviteToJoin(supervisor, title, description, researcher, text), email)


class ReqToJoinResearch(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, research, current_user):
        text = request.json.get('text', '')
        title = research['title']
        supervisor = research.supervisor
        user_name = current_user.name

        mailer.send(
            ReqToJoinSubj(user_name, title),
            ReqToJoin(supervisor.name, user_name, title, text), supervisor.email)

        return ok_msg('Request to join was send to {0}'.format(supervisor.email))
