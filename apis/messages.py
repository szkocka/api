import json

from flask import request
from flask.ext.restful import Resource
from google.appengine.api.taskqueue import taskqueue

from common.http_responses import ok, created, ok_msg
from common.insert_wraps import insert_forum, insert_message
from common.security import is_researcher, authenticate, is_admin, is_message_owner_or_admin
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

        add_task(message_key.id())

        return created(MessageIdJson(message_key))


class UpdateMessage(Resource):
    method_decorators = [is_message_owner_or_admin, insert_message, validate_request, authenticate]
    required_fields = ['message']  # used by validate_request

    def put(self, current_user, message):
        message.text = request.json['message']
        message.put()
        return ok_msg('Message updated')


class DeleteMessage(Resource):
    method_decorators = [is_message_owner_or_admin, insert_message, authenticate]

    def delete(self, current_user, message):
        message.status = StatusType.DELETED
        message.put()
        return ok_msg('Message deleted.')


def add_task(message_id):
    payload = {'message_id': message_id}
    taskqueue.add(url='/tasks/notify-new-message',
                  payload=json.dumps(payload),
                  headers={'Content-Type': 'application/json'})
