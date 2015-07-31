from flask.ext.restful import Resource

from security.authenticate import authenticate

class Me(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self, current_user):
        return current_user, 200
