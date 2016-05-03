from flask import request

from flask.ext.restful import Resource
from model.db import Research

from common.http_responses import ok_msg
from model.docs import ResearchIndex


class IndexResearch(Resource):
    def post(self):
        research_id = int(request.json['research_id'])
        research = Research.get(research_id)

        ResearchIndex(research).put()

        return ok_msg('Research indexed.')
