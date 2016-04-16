from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok
from common.prettify_responses import prettify_researches
from model.docs import ResearchIndex


class FindResearches(Resource):
    def get(self):
        args = request.args

        keyword = args.get('keyword', '*')
        status = args.get('status')
        tag = args.get('tag')
        page = args.get('page', 0)

        result = ResearchIndex.find(keyword, status, tag, page)

        return ok(
                {
                    'researches': prettify_researches(result)
                }
        )
