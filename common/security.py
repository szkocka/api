from functools import wraps

from flask import request
from itsdangerous import SignatureExpired, BadSignature

from common.http_responses import forbidden, unauthorized, bad_request
from common.util import verify_token, generate_token
from db.repository import get_user


class Token:
    def __init__(self, user_id):
        self.token = generate_token(user_id)

    def json(self):
        return {'token': self.token}


def authenticate(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            return unauthorized('Token not present.')

        authorization = request.headers['Authorization']
        token = authorization.replace('Bearer ', '')
        try:
            user_id = verify_token(token)
        except SignatureExpired:
            return unauthorized('Token expired.')
        except BadSignature:
            return unauthorized('Invalid token.')

        user = get_user(user_id)

        if not user:
            return unauthorized('User not found.')

        kwargs['current_user'] = user
        return func(*args, **kwargs)

    return wrapper


def is_researcher(func):
    def __is_researcher(research, current_user):
        researchers = research['researchers']
        return __is_supervisor(research, current_user) \
               or current_user.email() in researchers

    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs['current_user']

        if 'research' in kwargs:
            research = kwargs['research']
        elif 'forum':
            forum = kwargs['forum']
            research = forum.research
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

        if not __is_supervisor(research, current_user):
            return forbidden('You must be supervisor to call this API.')

        return func(*args, **kwargs)

    return wrapper


def __is_supervisor(research, current_user):
    return current_user.id == research.supervisor.id
