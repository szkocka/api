from flask import request
from flask.ext.restful import Resource
import logging

from common.http_responses import bad_request, created, ok, ok_msg, accepted
from common.insert_wraps import insert_user
from common.util import hash_password, get_relationship_types
from common.validation import validate_request
from common.security import Token, authenticate, is_admin
from model.db import User, Research, StatusType, Forum, Message
from model.resp import UserDetailsJson, ListUsers, ListUserResearchesJson, ListForumsJson, ListMessagesJson


class CreateUser(Resource):
    method_decorators = [validate_request]
    required_fields = ['email', 'name', 'password']  # used by validate_request

    def post(self):
        json_request = request.json
        email = json_request['email']
        name = json_request['name']
        password = json_request['password']
        cv = json_request.get('cv', '')

        user = User.by_email(email)
        if user:
            return bad_request('User with email {0} already exists'.format(email))

        user = User(name=name, email=email, cv=cv,
                    is_admin=False,
                    status=StatusType.ACTIVE,
                    hashed_password=hash_password(password))

        user_key = user.put()

        return created(Token(user_key.id()).json())


class UpdateUser(Resource):
    method_decorators = [authenticate]

    def put(self, current_user):
        json_request = request.json
        current_user.name = json_request.get('name', current_user.name)
        current_user.cv = json_request.get('cv', current_user.cv)

        current_user.put()

        return ok_msg('Profile updated.')


class UserDetails(Resource):
    method_decorators = [authenticate, insert_user]

    def get(self, current_user, user):
        supervisor_of = Research.by_supervisor(user.key)
        researcher_in = Research.by_researcher(user.key)

        return ok(UserDetailsJson(user, supervisor_of, researcher_in))


class ListAllUsers(Resource):
    method_decorators = [is_admin, authenticate]

    def get(self, current_user):
        cursor = request.args.get('cursor')
        users, cursor, _ = User.all(cursor)

        return ok(ListUsers(users, cursor))


class ListUserResearches(Resource):
    method_decorators = [is_admin, insert_user, authenticate]

    def get(self, current_user, user):
        relationship_types = get_relationship_types(user)
        cursor = request.args.get('cursor')
        users, cursor, _ = Research.by_user(user.key, cursor)

        return ok(ListUserResearchesJson(users, relationship_types, cursor))


class ListUserForums(Resource):
    method_decorators = [is_admin, insert_user, authenticate]

    def get(self, current_user, user):
        cursor = request.args.get('cursor')
        forums, cursor, _ = Forum.by_creator(user.key, cursor)

        return ok(ListForumsJson(forums, cursor))


class ListUserMessages(Resource):
    method_decorators = [is_admin, insert_user, authenticate]

    def get(self, current_user, user):
        cursor = request.args.get('cursor')
        messages, cursor, _ = Message.by_creator(user.key, cursor)

        return ok(ListMessagesJson(messages, cursor))


class UpdatePassword(Resource):
    method_decorators = [validate_request, authenticate]
    required_fields = ['newPassword', 'oldPassword']

    def put(self, current_user):
        json_request = request.json
        new_password = json_request['newPassword']
        old_password = json_request['oldPassword']
        hashed_old_password = hash_password(old_password)

        if current_user.hashed_password == hashed_old_password:
            hashed_new_password = hash_password(new_password)
            current_user.hashed_password = hashed_new_password
            current_user.put()

            return ok_msg('Password updated.')
        else:
            return bad_request('Incorrect old password.')


class DeleteUsers(Resource):
    method_decorators = [is_admin, authenticate]
    required_fields = ['users_ids']  # used by validate_request

    def post(self, current_user):
        json_request = request.json

        users_ids = json_request['users_ids']
        update_users_status(users_ids, StatusType.DELETED, True, True)

        return accepted("Provided users are deleted.")


class BanUsers(Resource):
    method_decorators = [is_admin, authenticate]
    required_fields = ['users_ids', 'ban_messages', 'ban_forums']  # used by validate_request

    def post(self, current_user):
        json_request = request.json

        users_ids = json_request['users_ids']
        ban_forums = bool(json_request['ban_forums'])
        ban_messages = bool(json_request['ban_messages'])

        update_users_status(users_ids, StatusType.BANNED, ban_forums, ban_messages)

        return accepted("Provided users are banned.")


def update_users_status(users_ids, status, ban_forums, ban_messages):
    for user_id in users_ids:
        user = User.get(user_id)
        user.status = status
        user.put()

        if ban_messages:
            update_messages_status(user, status)
        if ban_forums:
            update_forums_status(user, status)


def update_messages_status(user, status):
    messages = Message.by_creator2(user.key)

    for message in messages:
        message.status = status
        message.put()


def update_forums_status(user, status):
    forums = Forum.by_creator2(user.key)

    for forum in forums:
        forum.status = status
        forum.put()
