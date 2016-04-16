import logging
import os

from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok, created
from common.insert_wraps import insert_research
from common.validation import validate_request
from common.prettify_responses import prettify_researches, prettify_research
from common.security import authenticate, is_supervisor
from model.db import Research


class ListResearches(Resource):
    def get(self):
        return ok(
            {
                'researches': prettify_researches(Research.all())
            }
        )


class GetResearch(Resource):
    method_decorators = [insert_research]

    def get(self, research):
        return ok(prettify_research(research))


class AddResearch(Resource):
    method_decorators = [validate_request, authenticate]
    required_fields = ['title', 'area', 'description']  # used by validate_request

    def post(self, current_user):
        research = self.__create(current_user, request.json)

        return created(
            {
                'research_id': research.put().id()
            }
        )

    def __create(self, current_user, json):
        description = json['description']
        title = json['title']
        area = json['area']

        default_image_url = os.environ['DEFAULT_IMAGE']
        image_url = json.get('image_url', default_image_url)

        tags = json.get('tags', [])
        brief_desc = description.get('brief', '')
        detailed_desc = description.get('detailed', '')

        return Research(
                supervisor_key=current_user.key,
                title=title,
                area=area,
                tags=tags,
                status='active',
                brief_desc=brief_desc,
                detailed_desc=detailed_desc,
                image_url=image_url)


class UpdateResearch(Resource):
    method_decorators = [is_supervisor, insert_research, authenticate]

    def put(self, research, current_user):
        json = request.json

        research.title = json.get('title', research.title)
        research.tags = json.get('tags', research.tags)

        research.tags = json.get('tags', research.tags)
        research.area = json.get('area', research.area)
        research.status = json.get('status', research.status)
        research.image_url = json.get('image_url', research.image_url)

        description = json.get('description', {})
        research.brief_desc = description.get('brief', research.brief_desc)
        research.detailed_desc = description.get('detailed', research.detailed_desc)

        return ok(
            {
                'research_id': research.put().id()
            }
        )


class ListTags(Resource):
    def get(self):
        return ok({'tags': Research.all_tags()})
