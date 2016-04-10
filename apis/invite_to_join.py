from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok_msg
from common.insert_wraps import insert_research
from common.security import is_supervisor, authenticate
from common.validation import validate_request
from model.db import User, ResearchInvite
from emails import sender
from emails.views import InviteToJoinSubj, InviteToJoin


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
        research.researchers_keys.append(user.key)
        research.put()
        return user.name

    def __add_invite(self, research, recipient):
        invite = ResearchInvite(research_key=research.key,
                                email=recipient)
        invite.put()
        return recipient
