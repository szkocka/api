import logging
from functools import wraps

from flask import request
from itsdangerous import SignatureExpired, BadSignature

from common.http_responses import forbidden, unauthorized, bad_request
from common.util import TokenUtil
from model.db import User

TOKEN_UTIL = TokenUtil()


class Token:
    def __init__(self, user_id):
        self.token = TOKEN_UTIL.generate(user_id)

    def json(self):
        return {'token': self.token}


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info('Headers: ' + str(request.headers))
        if 'Authorization' not in request.headers:
            return unauthorized('Token not present.')

        authorization = request.headers['Authorization']
        token = authorization.replace('Bearer ', '')
        try:
            user_id = TOKEN_UTIL.verify(token)
        except SignatureExpired:
            return unauthorized('Token expired.')
        except BadSignature:
            return unauthorized('Invalid token.')

        user = User.get(int(user_id))

        if not user:
            return unauthorized('User not found.')

        kwargs['current_user'] = user
        return func(*args, **kwargs)

    return wrapper


def optional_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            kwargs['current_user'] = None
            return func(*args, **kwargs)

        authorization = request.headers['Authorization']
        token = authorization.replace('Bearer ', '')
        try:
            user_id = TOKEN_UTIL.verify(token)
        except SignatureExpired:
            return unauthorized('Token expired.')
        except BadSignature:
            return unauthorized('Invalid token.')

        user = User.get(int(user_id))

        if not user:
            return unauthorized('User not found.')

        kwargs['current_user'] = user
        return func(*args, **kwargs)

    return wrapper


def is_researcher(func):
    def __is_researcher(research, user):
        return user.is_supervisor_of(research) or user.is_researcher_of(research)

    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs['current_user']

        if 'research' in kwargs:
            research = kwargs['research']
        elif 'forum':
            forum = kwargs['forum']
            research = forum.research_key.get()
        else:
            return bad_request("Can't get info about research.")

        if not __is_researcher(research, current_user):
            return forbidden('You must be researcher to call this API.')

        return func(*args, **kwargs)

    return wrapper


def is_supervisor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        research = kwargs['research']
        current_user = kwargs['current_user']

        if not current_user.is_supervisor_of(research):
            return forbidden('You must be supervisor to call this API.')

        return func(*args, **kwargs)

    return wrapper


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs['current_user']

        logging.info('Current user: {0}'.format(current_user))
        if not current_user.is_admin:
            return forbidden('You must be admin to call this API.')

        return func(*args, **kwargs)

    return wrapper
