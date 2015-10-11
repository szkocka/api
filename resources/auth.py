from flask import request
from flask.ext.restful import Resource

from common.http_responses import unauthorized, ok
from common.util import hash_password
from common.validation import validate_request
from common.security import Token
from db.repository import find_user


class AuthLocalLogin(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'password']  # used by validate_request

    def post(self):
        email = request.json['email']
        hashed_pass = hash_password(request.json['password'])
        user = find_user(email, hashed_pass)

        if not user:
            return unauthorized('User not found.')

        return ok(Token(user.id).json())
