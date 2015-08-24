from datetime import datetime
from bson import ObjectId
from flask import request
from flask.ext.restful import Resource
from resources.prettify_responses import prettify_forums, prettify_forum, prettify_messages
from security.authenticate import authenticate


class ListForums(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.users = self.db['users']

    def get(self, research_id, current_user):
        forums = self.forums.find({'research': research_id})
        return {'forums': prettify_forums(self.users, forums)}, 200


class AddForum(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']

    def post(self, research_id, current_user):
        json = request.json

        forum_id = self.forums.insert_one({
            'createdBy': current_user.id(),
            'created': datetime.now(),
            'subject': json['subject'],
            'research': research_id
        }).inserted_id

        return {'forum_id': str(forum_id)}, 201

class GetForum(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.messages = self.db['messages']
        self.users = self.db['users']

    def get(self, forum_id, current_user):
        forum = self.forums.find_one({'_id': ObjectId(forum_id)})

        if forum is None:
            return {'message': 'Forum with ID: {0} not found.'.format(forum_id)}, 404

        messages = self.messages.find({'forum': forum_id})

        return {
            'forum': prettify_forum(self.users, forum),
            'messages': prettify_messages(self.users, messages)
        }, 200


class AddMessage(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.messages = self.db['messages']

    def post(self, forum_id, current_user):
        json = request.json

        message_id = self.messages.insert_one({
            'createdBy': current_user.id(),
            'created': datetime.now(),
            'message': json['message'],
            'forum': forum_id
        }).inserted_id

        return {'message_id': str(message_id)}, 201
