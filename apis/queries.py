import logging

from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok
from model.db import StatusType
from model.docs import ResearchIndex
from model.resp import ResearchesSearchResultJson


class FindResearches(Resource):
    def get(self):
        args = request.args
        logging.info(args)

        keyword = args.get('keyword')
        status = args.get('status', StatusType.ACTIVE)
        tag = args.get('tag')
        page = args.get('page', 0)

        researches = ResearchIndex.find(keyword, status, tag, page)
        return ok(ResearchesSearchResultJson(researches))
