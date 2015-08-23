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

        user_id = self.users.insert_one({
            'name': json['name'],
            'email': json['email'],
            'hashed_pass':  hash_password(json['password']),
            'provider': 'local',
            'role': 'user'
        }).inserted_id

        return Token(user_id).json(), 201
