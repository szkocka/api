from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok, created
from common.insert_wraps import insert_forum
from common.security import is_researcher, authenticate
from common.validation import validate_request
from model.db import Message, StatusType
from model.resp import ListMessagesJson, MessageIdJson


class ListMessages(Resource):
    method_decorators = [is_researcher, insert_forum, authenticate]

    def get(self, current_user, forum):
        cursor = request.args.get('cursor')
        messages, cursor, _ = Message.by_forum(forum.key, cursor)
        return ok(ListMessagesJson(messages, cursor))


class AddMessage(Resource):
    method_decorators = [is_researcher, insert_forum, validate_request, authenticate]
    required_fields = ['message']  # used by validate_request

    def post(self, current_user, forum):
        message = Message(
                creator_key=current_user.key,
                forum_key=forum.key,
                status=StatusType.ACTIVE,
                text=request.json['message'])

        message_key = message.put()
        current_user.posted_messages += 1
        current_user.put()
        return created(MessageIdJson(message_key))
