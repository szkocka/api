from boto.s3.key import Key, boto
from flask import request
from flask.ext.restful import Resource
from security.authenticate import authenticate


class Upload(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self, current_user):
        c = boto.connect_s3()
        b = c.get_bucket('srg-images')
        k = b.new_key('foobar3')
        k.set_contents_from_file(request.files['file'])

        return current_user.json(), 200
