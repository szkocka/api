from flask.ext.restful import Resource

from common.http_responses import ok
from common.security import authenticate


class Me(Resource):
    method_decorators = [authenticate]

    def get(self, current_user):
        return ok(
            {
                'user':
                    {
                        '_id': current_user.key.id(),
                        'name': current_user.name,
                        'email': current_user.email,
                        'role': 'admin' if current_user.is_admin else 'user',
                        'provider': 'local'
                    }
            }
        )
