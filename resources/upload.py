import uuid
from flask import request
from flask.ext.restful import Resource
from gcloud import storage

from common.http_responses import created
from common.security import authenticate

from flask import current_app as app
from google.appengine.api import app_identity


class Upload(Resource):
    method_decorators = [authenticate]

    def post(self, current_user):
        uploaded_file = request.files['file']
        app_id = app_identity.get_application_id()
        client = storage.Client(project=app_id)
        bucket = client.get_bucket(app.config['BUCKET_NAME'])

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
