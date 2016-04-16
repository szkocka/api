from flask import request

from flask.ext.restful import Resource
from model.db import ResearchInvite, User, Research

from common.http_responses import ok_msg
from model.docs import ResearchIndex


class ProcessResearchers(Resource):
    def post(self):
        researcher_id = int(request.json['researcher_id'])
        researcher = User.get(researcher_id)

        if researcher:
            for invite in ResearchInvite.by_email(researcher.email):
                research = invite.research_key.get()

                research.researchers_keys.append(researcher.key)
                research.put()

                invite.key.delete()

        return ok_msg('Researcher processed.')


class IndexResearch(Resource):
    def post(self):
        research_id = int(request.json['research_id'])
        research = Research.get(research_id)

        ResearchIndex(research).put()

        return ok_msg('Research indexed.')
