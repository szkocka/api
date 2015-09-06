from boto.s3.key import boto
from bson import ObjectId
from flask import request
from flask.ext.restful import Resource
from common.http_responses import created

from common.security import authenticate

BUCKET_NAME = 'srg-images'
IMAGE_TYPE = 'image/jpeg'

class Upload(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self, current_user):
        uploaded_file = request.files['file']

        s3connection = boto.connect_s3()
        bucket = s3connection.get_bucket(BUCKET_NAME)
        key = bucket.new_key('{0}.jpg'.format(str(ObjectId())))
        key.content_type = IMAGE_TYPE
        key.set_contents_from_file(uploaded_file)
        key.make_public()

        return created(
            {
                "url": key.generate_url(expires_in=0, query_auth=False, force_http=True)
            }
        )
