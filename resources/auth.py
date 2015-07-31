from flask import request
from flask.ext.restful import Resource
from common.util import hash_password, generate_token
from security.authenticate import Token


class AuthLocal(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.users = self.db['users']
        self.logger = kwargs['logger']

    def post(self):
        def login():
            json = request.json
            email = json['email']
            hashed_pass = hash_password(json['password'])

            user_id = self.users.find_one(
                {
                    'email': email,
                    'hashed_pass': hashed_pass
                },
                {'_id': True}
            )

            if user_id is None:
                return {'message': 'User not found.'}, 401

            return Token(generate_token(user_id)), 200

        return login()
