from flask import request
from flask.ext.restful import Resource

from common.http_responses import created, ok, ok_msg
from common.insert_wraps import insert_forum, insert_research
from common.validation import validate_request
from common.security import authenticate, is_researcher, is_admin
from model.db import Forum, StatusType
from model.resp import ForumIdJson, ListForumsJson, ForumJson


class ListForums(Resource):
    method_decorators = [is_researcher, insert_research, authenticate]

    def get(self, current_user, research):
        cursor = request.args.get('cursor')
        forums, cursor, _ = Forum.by_research(research.key, cursor)

        return ok(ListForumsJson(forums, cursor))


class AddForum(Resource):
    method_decorators = [is_researcher, insert_research, validate_request, authenticate]
    required_fields = ['subject']  # used by validate_request

    def post(self, current_user, research):
        forum = Forum(creator_key=current_user.key,
                      research_key=research.key,
                      status=StatusType.ACTIVE,
                      subject=request.json['subject'])

        forum_key = forum.put()
        current_user.created_forums += 1
        current_user.put()
        return created(ForumIdJson(forum_key))


class GetForum(Resource):
    method_decorators = [is_researcher, insert_forum, authenticate]

    def get(self, current_user, forum):
        return ok(ForumJson(forum))


class UpdateForum(Resource):
    method_decorators = [is_admin, insert_forum, validate_request, authenticate]
    required_fields = ['subject']  # used by validate_request

    def put(self, current_user, forum):
        forum.subject = request.json['subject']
        forum.put()
        return ok_msg('Forum is updated.')


class DeleteForum(Resource):
    method_decorators = [is_admin, insert_forum, authenticate]

    def delete(self, current_user, forum):
        forum.status = StatusType.DELETED
        forum.put()
        return ok_msg('Forum is deleted.')
