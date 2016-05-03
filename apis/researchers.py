from flask.ext.restful import Resource
from flask import request
from common.http_responses import ok_msg
from common.insert_wraps import insert_research, insert_user
from common.security import is_supervisor, authenticate
from common.validation import validate_request
from model.db import ResearchInvite
from emails import sender
from emails.views import InviteToJoinSubj, InviteToJoin


class RemoveResearcher(Resource):
    method_decorators = [is_supervisor, insert_research, insert_user, authenticate]

    def delete(self, current_user, research, user):
        research.researchers_keys.remove(user.key)
        research.put()

        return ok_msg('Researcher removed from research.')


class InviteResearcher(Resource):
    method_decorators = [is_supervisor, insert_research, validate_request, authenticate]
    required_fields = ['email']  # used by validate_request

    def post(self, research, current_user):
        recipient = request.json['email']
        text = request.json.get('text', '')
        supervisor = current_user.name
        title = research.title
        description = research.brief_desc

        researcher = self.__add_invite(research, recipient)

        subj = InviteToJoinSubj(supervisor, title)
        body = InviteToJoin(supervisor, title, description, researcher, text)
        sender.send_email(subj, body, recipient)

        return ok_msg("Invitation send to {0}".format(recipient))

    def __add_invite(self, research, recipient):
        invite = ResearchInvite(research_key=research.key, email=recipient)
        invite.put()

        return recipient
