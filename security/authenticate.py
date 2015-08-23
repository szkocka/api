from functools import wraps
from bson import ObjectId
from flask import request
from itsdangerous import SignatureExpired, BadSignature
from common.util import verify_token, handle_object_id, generate_token


class Token:
    def __init__(self, user_id):
        self.token = generate_token(user_id)

    def json(self):
        return {'token': self.token}

class CurrentUser:
    def __init__(self, user):
        self.user = user
        handle_object_id(self.user)
        del self.user['hashed_pass']

    def json(self):
        return self.__dict__

    def id(self):
        return self.user["_id"]

def authenticate(func):
    def find_user(user_id):
        users = func.im_self.db.users
        return users.find_one({'_id': ObjectId(user_id)})

    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            return {'message': "Token not present."}, 401

        authorization = request.headers['Authorization']
        token = authorization.replace('Bearer ', '')
        try:
            user_id = verify_token(token)
        except SignatureExpired:
            return {'message': "Token expired."}, 401
        except BadSignature:
            return {'message': 'Invalid token.'}, 401

        user = find_user(user_id)

        if user is None:
            return {'message': 'User not found.'}, 401

        kwargs["current_user"] = CurrentUser(user)
        return func(*args, **kwargs)

    return wrapper
