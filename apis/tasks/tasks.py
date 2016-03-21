from flask import request

from flask.ext.restful import Resource
from db.model import ResearchInvite, User

from common.http_responses import ok_msg


class ProcessResearchers(Resource):

    def post(self):
        json_str = request.json

        researcher_id = int(json_str['researcher_id'])
        researcher = User.get(researcher_id)

        if researcher:
            for invite in ResearchInvite.by_email(researcher.email):
                research = invite.research_key.get()

                research.researchers_keys.append(researcher.key)
                research.put()

                invite.key.delete()

        return ok_msg('Researcher processed.')
