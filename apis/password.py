import os
import uuid

from flask import request
from flask.ext.restful import Resource
import logging

from common.http_responses import ok_msg, bad_request, not_found
from common.validation import validate_request
from common.security import authenticate
from common.util import hash_password
from emails import sender
from emails.views import ResetPasswordSubj, ResetPasswordBody
from model.db import User, ChangePasswordRequest


class UpdatePassword(Resource):
    method_decorators = [validate_request, authenticate]
    required_fields = ['newPassword', 'oldPassword']

    def put(self, current_user):
        json_request = request.json
        new_password = json_request['newPassword']
        old_password = json_request['oldPassword']
        hashed_old_password = hash_password(old_password)

        if current_user.hashed_password == hashed_old_password:
            hashed_new_password = hash_password(new_password)
            current_user.hashed_password = hashed_new_password
            current_user.put()

            return ok_msg('Password updated.')
        else:
            return bad_request('Incorrect old password.')


class ResetPassword(Resource):
    method_decorators = [validate_request]
    required_fields = ['email']

    def post(self):
        json_request = request.json
        email = json_request['email']

        user = User.by_email(email)

        if user:
            token = str(uuid.uuid4())
            base_url = os.environ['BASE_UI_URL']
            url = base_url + '&token=' + token
            user_name = user.name

            ChangePasswordRequest(user_key=user.key, token=token).put()

            subj = ResetPasswordSubj(user_name)
            body = ResetPasswordBody(user_name, url)
            sender.send_email(subj, body, email)
            return ok_msg('Emails with instructions is sent.')
        else:
            return not_found('User not found in system.')


class NewPassword(Resource):
    method_decorators = [validate_request]
    required_fields = ['newPassword', 'token']

    def post(self):
        json_request = request.json
        token = json_request['token']
        new_password = json_request['newPassword']

        change_password = ChangePasswordRequest.by_token(token)

        if change_password:
            hashed_new_password = hash_password(new_password)
            user = change_password.user_key.get()
            user.hashed_password = hashed_new_password
            user.put()
            change_password.key.delete()

            return ok_msg('Password is reset.')
        else:
            return not_found('User didn\'t requested password reset.')
