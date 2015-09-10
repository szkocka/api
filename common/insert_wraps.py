from functools import wraps
from bson import ObjectId
from common.http_responses import bad_request, forum_not_found, research_not_found
from common.util import im_self


def insert_research(func):
    def __find_research(_id):
        researches = im_self(func).db.researches
        return researches.find_one(
            {
                '_id': ObjectId(_id)
            }
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'research_id' not in kwargs:
            return bad_request('To use insert_research wrapper research_id must be in url.')

        _id = kwargs['research_id']
        research = __find_research(_id)

        if research is None:
            return research_not_found(_id)

        del kwargs['research_id']
        kwargs['research'] = research

        return func(*args, **kwargs)
    return wrapper


def insert_forum(func):
    def __find_forum(_id):
        forums = im_self(func).forums
        return forums.find_one(
            {
                '_id': ObjectId(_id)
            }
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'forum_id' not in kwargs:
            return bad_request('To use insert_forum wrapper forum_id must be in url.')

        _id = kwargs['forum_id']
        forum = __find_forum(_id)

        if forum is None:
            return forum_not_found(_id)

        del kwargs['forum_id']
        kwargs['forum'] = forum

        return func(*args, **kwargs)
    return wrapper
