from flask import request
from flask.ext.restful import Resource
from common.http_responses import unauthorized, ok

from common.util import hash_password
from common.validation import validate_request
from common.security import Token


class AuthLocalLogin(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'password']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.users = self.db['users']
        self.logger = kwargs['logger']

    def post(self):
        email, hashed_pass = self.__request_fields()
        user = self.__find_user(email, hashed_pass)

        if user is None:
            return unauthorized('User not found.')

        return ok(Token(user['_id']).json())

    def __request_fields(self):
        json = request.json
        return json['email'], hash_password(json['password'])

    def __find_user(self, email, hashed_pass):
        return self.users.find_one(
            {
                'email': email,
                'hashed_pass': hashed_pass
            },
            {
                '_id': True
            }
        )
