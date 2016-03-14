import json

from flask import request
from flask.ext.restful import Resource

from common.http_responses import bad_request, created
from common.util import hash_password
from common.validation import validate_request
from common.security import Token
from db.model import User
from google.appengine.api import taskqueue


class CreateUser(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'name', 'password']  # used by validate_request

    def post(self):
        email = request.json['email']

        user = User.by_email(email)
        if user:
            return bad_request('User with email {0} already exists'.format(email))

        name = request.json['name']
        hashed_pass = hash_password(request.json['password'])

        user = User(name=name, email=email,
                    is_admin=False,
                    hashed_password=hashed_pass)

        user_key = user.put()

        taskqueue.add(url='/async/process-researchers',
                      payload=json.dumps({
                          'researcher_id': user_key.id()
                      }),
                      headers={
                          'Content-Type': 'application/json'
                      }
        )

        return created(Token(user_key.id()).json())
