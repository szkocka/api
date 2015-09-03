from flask import request
from flask.ext.restful import Resource
from common.util import hash_password
from common.validation import validate_request
from security.authenticate import Token


class AuthLocalLogin(Resource):
    method_decorators = [validate_request]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.users = self.db['users']
        self.logger = kwargs['logger']
        self.required_fields = ['email', 'password']

    def post(self):
        email, hashed_pass = self.__fields(request.json)
        user = self.__find_user(email, hashed_pass)

        if user is None:
            return {'message': 'User not found.'}, 401

        return Token(user['_id']).json(), 200

    def __fields(self, json):
        return json['email'], hash_password(json['password'])

    def __find_user(self, email, hashed_pass):
        return self.users.find_one(
            {
                'email': email,
                'hashed_pass': hashed_pass
            },
            {'_id': True}
        )
