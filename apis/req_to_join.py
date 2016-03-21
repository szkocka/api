from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok_msg
from common.insert_wraps import insert_research
from common.security import authenticate
from emails import sender
from emails.views import ReqToJoinSubj, ReqToJoin


class ReqToJoinResearch(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, research, current_user):
        supervisor = research.supervisor_key.get()

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
