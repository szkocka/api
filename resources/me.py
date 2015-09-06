from flask.ext.restful import Resource
from common.http_responses import ok

from common.security import authenticate

class Me(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self, current_user):
        return ok(current_user.json())
