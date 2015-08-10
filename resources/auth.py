from flask import request
from flask.ext.restful import Resource
from common.util import hash_password, generate_token


class AuthLocalLogin(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.users = self.db['users']
        self.logger = kwargs['logger']

    def post(self):
        json = request.json
        email = json['email']
        hashed_pass = hash_password(json['password'])

        user = self.users.find_one(
            {
                'email': email,
                'hashed_pass': hashed_pass
            },
            {'_id': True}
        )

        if user is None:
            return {'message': 'User not found.'}, 401

        return {'token': generate_token(user['_id'])}, 200
