import os
import json
from flask import request
from flask.ext.restful import Resource
from google.appengine.api import taskqueue

from common.http_responses import ok, created, ok_msg
from common.insert_wraps import insert_research
from common.util import get_relationship_types
from common.validation import validate_request
from common.security import authenticate, is_supervisor, optional_authenticate
from model.db import Research, ResearchRelationship, RelationshipType, StatusType, Forum, Message
from model.docs import ResearchIndex
from model.resp import TagsJson, ResearchIdJson, ListResearchesJson, ResearchDetailsJson


class ListResearches(Resource):
    method_decorators = [optional_authenticate]

    def get(self, current_user):
        relationship_types = get_relationship_types(current_user)

        cursor = request.args.get('cursor')
        researches, cursor, _ = Research.all(cursor)

        return ok(ListResearchesJson(researches, relationship_types, cursor))


class GetResearch(Resource):
    method_decorators = [insert_research, optional_authenticate]

    def get(self, research, current_user):
        relationship_types = self.__get_relationship_type(current_user, research)
        return ok(ResearchDetailsJson(research, relationship_types))

    def __get_relationship_type(self, current_user, research):
        relationship_types = {}
        if current_user:
            relationship = ResearchRelationship.get(research.key, current_user.email)
            if relationship:
                relationship_types[research.key.id()] = relationship.type

        return relationship_types


class AddResearch(Resource):
    method_decorators = [validate_request, authenticate]
    required_fields = ['title', 'area', 'description']  # used by validate_request

    def post(self, current_user):
        research_key = self.__create(current_user, request.json)
        self.__add_relationship(research_key, current_user)
        current_user.supervisor_in += 1
        current_user.put()

        add_task(research_key)
        return created(ResearchIdJson(research_key))

    def __add_relationship(self, research_key, current_user):
        ResearchRelationship(research_key=research_key,
                             user_email=current_user.email,
                             type=RelationshipType.SUPERVISOR).put()

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
                status=StatusType.ACTIVE,
                brief_desc=brief_desc,
                detailed_desc=detailed_desc,
                image_url=image_url).put()


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

        research_key = research.put()
        add_task(research_key)

        return ok(ResearchIdJson(research_key).js())


class DeleteResearch(Resource):
    method_decorators = [is_supervisor, insert_research, authenticate]

    def delete(self, research, current_user):
        research.status = StatusType.DELETED
        research.put()

        forums = Forum.by_research2(research.key)

        for forum in forums:
            forum.status = StatusType.DELETED
            forum.put()

            messages = Message.by_forum2(forum.key)

            for message in messages:
                message.status = StatusType.DELETED
                message.put()

        ResearchIndex(research).delete()

        return ok_msg('Research is deleted.')


class ListTags(Resource):
    def get(self):
        tags = Research.all_tags()
        return ok(TagsJson(tags))


def add_task(research_key):
    payload = ResearchIdJson(research_key).js()
    taskqueue.add(url='/tasks/index-research',
                  payload=json.dumps(payload),
                  headers={'Content-Type': 'application/json'})
