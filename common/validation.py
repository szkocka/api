from functools import wraps
from flask import request


def validate_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        json = request.json
        for field in func.im_self.required_fields:
            if field not in json:
                msg = 'Field "{0}" is required.'.format(field)
                return {'message': msg}, 400

        return func(*args, **kwargs)

    return wrapper
