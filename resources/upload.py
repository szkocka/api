from flask import request
from flask.ext.restful import Resource
from gcloud import storage

from common.http_responses import created
from common.security import authenticate

BUCKET_NAME = 'szkocka-images-test'
IMAGE_TYPE = 'image/jpeg'
PROJECT_ID = 'szkocka-1080'


class Upload(Resource):
    #method_decorators = [authenticate]

    def post(self):
        uploaded_file = request.files['file']
        client = storage.Client(project=PROJECT_ID)
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob('my-test-file.jpg')
        blob.upload_from_file(uploaded_file, content_type=IMAGE_TYPE)

        return created(
            {
                'url': blob.public_url
            }
        )
