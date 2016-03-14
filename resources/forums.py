from flask import request
from flask.ext.restful import Resource

from common.http_responses import created, ok
from common.insert_wraps import insert_forum, insert_research
from common.prettify_responses import prettify_forums, prettify_forum, prettify_messages
from common.validation import validate_request
from common.security import authenticate, is_researcher
from db.model import Forum, Message


class ListForums(Resource):
    method_decorators = [is_researcher, insert_research, authenticate]

    def get(self, current_user, research):
        forums = Forum.by_research(research.key)
        return ok(
            {
                'forums': prettify_forums(forums)
            }
        )


class AddForum(Resource):
    method_decorators = [is_researcher, insert_research, validate_request, authenticate]
    required_fields = ['subject']  # used by validate_request

    def post(self, current_user, research):
        forum = Forum(creator_key=current_user.key,
                      research_key=research.key,
                      subject=request.json['subject'])

        return created(
            {
                'forum_id': forum.put().id()
            }
        )


class GetForum(Resource):
    method_decorators = [is_researcher, insert_forum, authenticate]

    def get(self, current_user, forum):
        messages = Message.by_forum(forum.key)
        return ok(
            {
                'forum': prettify_forum(forum),
                'messages': prettify_messages(messages)
            }
        )


class AddMessage(Resource):
    method_decorators = [is_researcher, insert_forum, validate_request, authenticate]
    required_fields = ['message']  # used by validate_request

    def post(self, current_user, forum):
        message = Message(
                creator_key=current_user.key,
                forum_key=forum.key,
                text=request.json['message'])

        return created(
            {
                'message_id': message.put().id()
            }
        )
