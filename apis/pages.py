from flask.ext.restful import Resource
from flask import request

from common.http_responses import ok_msg, ok
from common.security import is_admin, authenticate
from common.validation import validate_request
from model.db import AboutPage


class UpdateAboutPage(Resource):
    method_decorators = [is_admin, authenticate, validate_request]
    required_fields = ['content']  # used by validate_request

    def post(self, current_user):
        content = request.json['content']
        about_page = AboutPage(id=1, content=content)
        about_page.put()

        return ok_msg('About page is updated.')


class GetAboutPage(Resource):
    def get(self):
        about_page = AboutPage.get(1)
        return ok({'content': about_page.content})
