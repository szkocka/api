from flask import request
from flask.ext.restful import Resource
from common.http_responses import bad_request, created

from common.util import hash_password
from common.validation import validate_request
from common.security import Token


class CreateUser(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'name', 'password']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.users = self.db['users']
        self.logger = kwargs['logger']

    def post(self):
        name, email, hashed_pass = self.__request_fields()

        if self.__user_exist(email):
            return bad_request('User with email {0} already exists'.format(email))

        new_user = self.__create(name, email, hashed_pass)
        user_id = self.__save(new_user)

        return created(Token(user_id).json())

    def __save(self, new_user):
        return self.users.insert_one(new_user).inserted_id

    def __create(self, name, email, hashed_pass):
        return {
            'name': name,
            'email': email,
            'hashed_pass': hashed_pass,
            'provider': 'local',
            'role': 'user'
        }

    def __request_fields(self):
        json = request.json

        hashed_pass = hash_password(json['password'])
        return json['name'], json['email'], hashed_pass

    def __user_exist(self, email):
        user = self.users.find_one(
            {
                'email': email
            }
        )
        return user is not None
