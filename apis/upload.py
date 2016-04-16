import os
import uuid
from flask import request
from flask.ext.restful import Resource
from gcloud import storage

from common.http_responses import created
from common.security import authenticate

from google.appengine.api.app_identity import get_application_id


class UploadImage(Resource):
    method_decorators = [authenticate]

    def __init__(self):
        client = storage.Client(project=get_application_id())
        bucket_name = os.environ['IMAGES_BUCKET']
        self.bucket = client.get_bucket(bucket_name)

    def post(self, current_user):
        image = request.files['file']
        blob_url = self.__store_image(image)

        return created(
                {
                    'url': blob_url.replace('https://', 'http://')
                }
        )

    def __store_image(self, image):
        blob_name = '{0}.jpg'.format(str(uuid.uuid1()))
        blob = self.bucket.blob(blob_name)

        blob.upload_from_file(image,
                              content_type=image.content_type,
                              size=image.__sizeof__())
        blob.make_public()

        return blob.public_url
