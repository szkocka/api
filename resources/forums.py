from datetime import datetime
from bson import ObjectId
from flask import request
from flask.ext.restful import Resource
from common.util import is_supervisor
from resources.prettify_responses import prettify_forums, prettify_forum, prettify_messages
from security.authenticate import authenticate


class ListForums(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.users = self.db['users']
        self.researches = self.db['researches']

    def get(self, research_id, current_user):
        if not is_researcher(self.researches, research_id, current_user):
            return {'message': 'You must be researcher to list forums.'}, 403

        forums = self.forums.find({'research': research_id})
        return {'forums': prettify_forums(self.users, forums)}, 200


class AddForum(Resource):
    method_decorators = [authenticate]

    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.forums = self.db['forums']
        self.researches = self.db['researches']

    def post(self, research_id, current_user):
        if not is_researcher(self.researches, research_id, current_user):
            return {'message': 'You must be researcher to add forum.'}, 403

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
        self.researches = self.db['researches']

    def get(self, forum_id, current_user):
        forum = self.forums.find_one({'_id': ObjectId(forum_id)})

        if forum is None:
            return {'message': 'Forum with ID: {0} not found.'.format(forum_id)}, 404

        if not is_researcher(self.researches, forum['research'], current_user):
            return {'message': 'You must be researcher to get forum.'}, 403

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
        self.researches = self.db['researches']

    def post(self, forum_id, current_user):
        forum = self.forums.find_one({'_id': ObjectId(forum_id)})

        if forum is None:
            return {'message': 'Forum with ID: {0} not found.'.format(forum_id)}, 404

        if not is_researcher(self.researches, forum['research'], current_user):
            return {'message': 'You must be researcher to add message.'}, 403

        json = request.json

        message_id = self.messages.insert_one({
            'createdBy': current_user.id(),
            'created': datetime.now(),
            'message': json['message'],
            'forum': forum_id
        }).inserted_id

        return {'message_id': str(message_id)}, 201


def is_researcher(researches, research_id, current_user):
    research = researches.find_one({'_id': ObjectId(research_id)})

    return is_supervisor(current_user, research) \
           or current_user.email() in research['researchers']
