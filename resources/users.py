from flask import request
from flask.ext.restful import Resource
from common.util import hash_password
from common.validation import validate_request
from security.authenticate import Token


class CreateUser(Resource):
    method_decorators = [validate_request]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.users = self.db['users']
        self.logger = kwargs['logger']
        self.required_fields = ['email', 'name', 'password']

    def post(self):
        name, email, hashed_pass = self.__fields(request.json)

        if self.__user_exist(email):
            return {'message': 'User with email {0} already exists'.format(email)}, 400

        new_user = self.__create(name, email, hashed_pass)
        user_id = self.__save(new_user)

        return Token(user_id).json(), 201

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

    def __fields(self, json):
        hashed_pass = hash_password(json['password'])
        return json['name'], json['email'], hashed_pass

    def __user_exist(self, email):
        user = self.users.find_one({'email': email})
        return user is not None
