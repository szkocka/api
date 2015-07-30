from flask.ext.restful import Resource
from flask import request

class Researches(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):
        return request.json

    def get(self):
        return "11"
