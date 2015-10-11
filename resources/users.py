from flask import request
from flask.ext.restful import Resource

from app import db
from common.http_responses import bad_request, created
from common.util import hash_password
from common.validation import validate_request
from common.security import Token
from db.model import User


class CreateUser(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'name', 'password']  # used by validate_request

    def post(self):
        #sql.create_all()

        email = request.json['email']

        if db.find_user_by_email(email):
            return bad_request('User with email {0} already exists'.format(email))

        name = request.json['name']
        hashed_pass = hash_password(request.json['password'])

        user = User(name, email, hashed_pass)

        db.save(user)
        return created(Token(user.id).json())
