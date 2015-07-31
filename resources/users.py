from flask import request
from flask.ext.restful import Resource
from common.util import hash_password, generate_token
from security.authenticate import Token


class Users(Resource):
    def __init__(self, **kwargs):
        self.users = kwargs['db']['users']
        self.logger = kwargs['logger']

    def post(self):
        def create_user():
            json = request.json

            user_id = self.users.insert_one({
                'name': json['name'],
                'email': json['email'],
                'hashed_pass':  hash_password(json['password']),
                'provider': 'local',
                'role': 'user'
            }).inserted_id

            return Token(generate_token(user_id)), 201

        return create_user()
