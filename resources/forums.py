from datetime import datetime

from flask import request
from flask.ext.restful import Resource
from common.http_responses import created, ok
from common.insert_wraps import insert_forum, insert_research

from common.prettify_responses import prettify_forums, prettify_forum, prettify_messages
from common.validation import validate_request
from common.security import authenticate, is_researcher


class ListForums(Resource):
    method_decorators = [authenticate, insert_research, is_researcher]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.users = self.db['users']
        self.researches = self.db['researches']

    def get(self, research, current_user):
        forums = self.__find_forums(research)

        return ok(
            {
                'forums': prettify_forums(self.users, forums)
            }
        )

    def __find_forums(self, research):
        forums = self.forums.find(
            {
                'research': research['_id']
            }
        )
        return forums


class AddForum(Resource):
    method_decorators = [authenticate, validate_request, insert_research, is_researcher]
    required_fields = ['subject']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.researches = self.db['researches']

    def post(self, research, current_user):
        forum = self.__create_forum(current_user, research)
        forum_id = self.__save(forum)

        return created(
            {
                'forum_id': str(forum_id)
            }
        )

    def __save(self, forum):
        return self.forums.insert_one(forum).inserted_id

    def __create(self, current_user, research):
        json = request.json
        return {
            'createdBy': current_user.id(),
            'created': datetime.now(),
            'subject': json['subject'],
            'research': research['_id']
        }


class GetForum(Resource):
    method_decorators = [authenticate, insert_forum, is_researcher]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.messages = self.db['messages']
        self.users = self.db['users']
        self.researches = self.db['researches']

    def get(self, forum, current_user):
        messages = self.__find_messages(forum)

        return ok(
            {
                'forum': prettify_forum(self.users, forum),
                'messages': prettify_messages(self.users, messages)
            }
        )

    def __find_messages(self, forum):
        messages = self.messages.find(
            {
                'forum': forum['_id']
            }
        )
        return messages


class AddMessage(Resource):
    method_decorators = [authenticate, validate_request, insert_forum, is_researcher]
    required_fields = ['message']  # used by validate_request

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.messages = self.db['messages']
        self.researches = self.db['researches']

    def post(self, forum, current_user):
        message = self.__create(current_user, forum)
        message_id = self.__save(message)

        return created(
            {
                'message_id': str(message_id)
            }
        )

    def __save(self, message):
        return self.messages.insert_one(message).inserted_id

    def __create(self, current_user, forum):
        json = request.json
        return {
            'createdBy': current_user.id(),
            'created': datetime.now(),
            'message': json['message'],
            'forum': forum['_id']
        }
