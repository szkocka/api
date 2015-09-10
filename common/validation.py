from functools import wraps
from flask import request
from common.util import im_self


def validate_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        json = request.json
        for field in im_self(func).required_fields:
            if field not in json:
                msg = 'Field "{0}" is required.'.format(field)
                return {'message': msg}, 400
        return func(*args, **kwargs)
    return wrapper
