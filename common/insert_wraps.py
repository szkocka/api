from functools import wraps

from common.http_responses import bad_request, forum_not_found, research_not_found
from db.repository import get_research, get_forum


def insert_research(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'research_id' not in kwargs:
            return bad_request('To use insert_research wrapper research_id must be in url.')

        _id = kwargs['research_id']
        research = get_research(_id)

        if research is None:
            return research_not_found(_id)

        del kwargs['research_id']
        kwargs['research'] = research

        return func(*args, **kwargs)
    return wrapper


def insert_forum(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'forum_id' not in kwargs:
            return bad_request('To use insert_forum wrapper forum_id must be in url.')

        _id = kwargs['forum_id']
        forum = get_forum(_id)

        if forum is None:
            return forum_not_found(_id)

        del kwargs['forum_id']
        kwargs['forum'] = forum

        return func(*args, **kwargs)
    return wrapper
