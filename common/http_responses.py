from model.resp import BaseJsonResponce


def ok_msg(msg):
    return {'message': msg}, 200


def ok(obj):
    if isinstance(obj, BaseJsonResponce):
        return obj.js(), 200
    return obj, 200


def created(obj):
    if isinstance(obj, BaseJsonResponce):
        return obj.js(), 201
    return obj, 201


def accepted(msg):
    return {'message': msg}, 202


def bad_request(msg):
    return {'message': msg}, 400


def unauthorized(msg):
    return {'message': msg}, 401


def forbidden(msg):
    return {'message': msg}, 403


def not_found(msg):
    return {'message': msg}, 404


def forum_not_found(_id):
    msg = 'Forum with ID: {0} not found.'.format(_id)
    return not_found(msg)


def message_not_found(_id):
    msg = 'Message with ID: {0} not found.'.format(_id)
    return not_found(msg)

def user_not_found(_id):
    msg = 'User with ID: {0} not found.'.format(_id)
    return not_found(msg)


def research_not_found(_id):
    msg = 'Research with ID: {0} not found.'.format(_id)
    return not_found(msg)
