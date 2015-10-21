from flask import request
from flask.ext.restful import Resource

from common.http_responses import bad_request, created
from common.util import hash_password
from common.validation import validate_request
from common.security import Token
from db.model import User, InvitedResearcher
from db.repository import find_user_by_email, save, get_research, update, find_invited_researchers_by_email, delete


class CreateUser(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'name', 'password']  # used by validate_request

    def post(self):
        #sql.create_all()

        email = request.json['email']

        if find_user_by_email(email):
            return bad_request('User with email {0} already exists'.format(email))

        name = request.json['name']
        hashed_pass = hash_password(request.json['password'])

        user = User(name, email, hashed_pass)

        save(user)
        return created(Token(user.id).json())


    def add_to_researches(self, user):
        invited_researchers = find_invited_researchers_by_email(user.email)

        for invited_researcher in invited_researchers:
            research = invited_researcher.research
            user.researches.append(research)
            delete(invited_researcher)
