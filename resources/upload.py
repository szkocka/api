import uuid
from flask import request
from flask.ext.restful import Resource
from gcloud import storage

from common.http_responses import created
from common.security import authenticate

from flask import current_app as app


class Upload(Resource):
    method_decorators = [authenticate]

    def post(self):
        uploaded_file = request.files['file']
        client = storage.Client(project=app.config.PROJECT_ID)
        bucket = client.get_bucket(app.config.BUCKET_NAME)

        blob = bucket.blob('{0}.jpg'.format(str(uuid.uuid1())))
        blob.upload_from_file(uploaded_file,
                              content_type=uploaded_file.content_type,
                              size=uploaded_file.__sizeof__())
        blob.make_public()

        https_url = blob.public_url
        http_url = https_url.replace('https://', 'http://')

        return created(
            {
                'url': http_url
            }
        )
