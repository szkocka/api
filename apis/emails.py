from emails import sender
from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok_msg
from common.insert_wraps import insert_research
from common.validation import validate_request
from common.security import authenticate, is_supervisor
from db.model import ResearchInvite, User
from emails.views import ReqToJoinSubj, ReqToJoin, InviteToJoinSubj, InviteToJoin


class InviteToJoinResearch(Resource):
    method_decorators = [is_supervisor, insert_research, validate_request, authenticate]
    required_fields = ['email']  # used by validate_request

    def post(self, research, current_user):
        recipient = request.json['email']
        text = request.json.get('text', '')
        supervisor = current_user.name
        title = research.title,
        description = research.brief_desc

        user = User.by_email(recipient)
        if user:
            researcher = self.__add_researcher(research, user)
        else:
            researcher = self.__add_invite(research, recipient)

        sender.send_email(
            InviteToJoinSubj(supervisor, title),
            InviteToJoin(supervisor, title, description, researcher, text),
            recipient
        )

        return ok_msg("Invitation send to {0}".format(recipient))

    def __add_researcher(self, research, user):
        research.researchers_keys.append(user.key())
        research.put()
        return user.name

    def __add_invite(self, research, recipient):
        invite = ResearchInvite(research, recipient)
        invite.put()
        return recipient


class ReqToJoinResearch(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, research, current_user):
        supervisor = research.supervisor

        user_name = current_user.name

        recipient = supervisor.email
        supervisor_name = supervisor.name

        title = research.title
        text = request.json.get('text', '')

        sender.send_email(
                ReqToJoinSubj(user_name, title),
                ReqToJoin(user_name, title, supervisor_name, text),
                recipient
        )

        return ok_msg('Request was send to {0}'.format(recipient))
