from flask import request
from flask.ext.restful import Resource

from common.http_responses import bad_request, created
from common.util import hash_password
from common.validation import validate_request
from common.security import Token
from db.model import User, InvitedResearcher


class CreateUser(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'name', 'password']  # used by validate_request

    def post(self):
        email = request.json['email']

        if User.by_email(email):
            return bad_request('User with email {0} already exists'.format(email))

        name = request.json['name']
        hashed_pass = hash_password(request.json['password'])

        user = User(name, email, hashed_pass)

        user_key = user.put()
        self.__add_to_researches(user)

        return created(Token(user_key.id()).json())


    def __add_to_researches(self, user):
        invited_researchers = InvitedResearcher.by_email(user.email)

        for invited_researcher in invited_researchers:
            research = invited_researcher.research
            user.researches.append(research)
            invited_researcher.key().delete()
