from flask import request
from flask.ext.restful import Resource
from common.util import hash_password, new_token


class AuthLocal(Resource):
    def __init__(self, **kwargs):
        self.users = kwargs['db']['users']
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
                {
                    '_id': True
                }
            )
            return {'token': new_token(user_id)}, 200

        return login()
