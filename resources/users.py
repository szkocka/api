from flask import request
from flask.ext.restful import Resource
from common.util import hash_password, new_token

class Users(Resource):
    def __init__(self, **kwargs):
        self.users = kwargs['db']['users']
        self.logger = kwargs['logger']

    def post(self):
        def create_user():
            json = request.json

            name = json['name']
            email = json['email']
            hashed_pass = hash_password(json['password'])

            user_id = self.users.insert_one({
                'name': name,
                'email': email,
                'hashed_pass': hashed_pass
            }).inserted_id

            return {'token': new_token(user_id)}, 201

        return create_user()
