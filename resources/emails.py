import json

from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok_msg
from common.insert_wraps import insert_research
from common.validation import validate_request
from common.security import authenticate, is_supervisor
from db.model import ResearchInvite, User
from google.appengine.api import taskqueue


class InviteToJoinResearch(Resource):
    method_decorators = [is_supervisor, insert_research, validate_request, authenticate]
    required_fields = ['email']  # used by validate_request

    def post(self, research, current_user):
        email = request.json['email']
        text = request.json.get('text', '')
        supervisor = current_user.name

        user = User.by_email(email)
        if user:
            research.researchers_keys.append(user.key())
            research.put()
            researcher = user.name
        else:
            ResearchInvite(research, email).put()
            researcher = email

        email_payload = {
            'researcher': researcher,
            'supervisor': supervisor,
            'recipient': email,
            'title': research.title,
            'description': research.brief_desc,
            'text': text
        }

        send(
            InviteToJoinSubj(email_payload),
            InviteToJoin(email_payload),
            email
        )

        return ok_msg("Invitation send to {0}".format(email))


class ReqToJoinResearch(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, research, current_user):
        supervisor = research.supervisor

        taskqueue.add(url='/join-req',
                      payload=json.dumps({
                        'user_name': current_user.name,
                        'supervisor_name': supervisor.name,
                        'recipient': supervisor.email,
                        'title': research.title,
                        'text': request.json.get('text', '')
                      }),
                      headers={
                          'Content-Type': 'application/json'
                      },
                      target='emails')

        return ok_msg('Request to join was send to {0}'.format(supervisor.email))

class InviteToJoinResearch(Resource):

    def post(self):


        return ok_msg('OK')


class ReqToJoinResearch(Resource):

    def post(self):
        send(
                ReqToJoinSubj(request.json),
                ReqToJoin(request.json),
                request.json['recipient']
        )

        return ok_msg('OK')


def send(subj_view, body_view, recipient):
    renderer = pystache.Renderer()

    subj = renderer.render(subj_view)
    body = renderer.render(body_view)

    logging.info('Sending email')
    mail.send_mail(sender=app.config['FROM_EMAIL'],
                   to=recipient, subject=subj, body=body)