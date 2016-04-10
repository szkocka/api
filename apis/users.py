import json

from flask import request
from flask.ext.restful import Resource

from common.http_responses import bad_request, created, ok
from common.insert_wraps import insert_user
from common.util import hash_password
from common.validation import validate_request
from common.security import Token, authenticate
from model.db import User, Research
from google.appengine.api import taskqueue

from model.resp import UserDetailsJson


class CreateUser(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'name', 'password']  # used by validate_request

    def post(self):
        json_request = request.json
        email = json_request['email']
        name = json_request['name']
        password = json_request['password']
        cv = json_request.get('cv', '')

        user = User.by_email(email)
        if user:
            return bad_request('User with email {0} already exists'.format(email))

        user = User(name=name, email=email, cv=cv,
                    is_admin=False,
                    hashed_password=hash_password(password))

        user_key = user.put()

        taskqueue.add(url='/tasks/process-researchers',
                      payload=json.dumps({
                          'researcher_id': user_key.id()
                      }),
                      headers={
                          'Content-Type': 'application/json'
                      }
        )

        return created(Token(user_key.id()).json())


class UserDetails(Resource):
    method_decorators = [authenticate, insert_user]

    def get(self, current_user, user):
        supervisor_of = Research.by_supervisor(user.key)
        researcher_in = Research.by_researcher(user.key)

        return ok(UserDetailsJson(user, supervisor_of, researcher_in))