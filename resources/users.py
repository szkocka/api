from flask import request
from flask.ext.restful import Resource
from common.util import hash_password, generate_token
from security.authenticate import Token


class CreateUser(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.users = self.db['users']
        self.logger = kwargs['logger']

    def post(self):
        json = request.json

        email = json['email']

        if self.users.find_one({'email': email}) is not None:
            return {'message': 'User with email {0} already exists'.format(email)}, 400

        new_user = {
            'name': json['name'],
            'email': email,
            'hashed_pass':  hash_password(json['password']),
            'provider': 'local',
            'role': 'user'
        }
        user_id = self.users.insert_one(new_user).inserted_id

        return Token(user_id).json(), 201
