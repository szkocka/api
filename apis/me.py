from flask.ext.restful import Resource

from common.http_responses import ok, ok_msg, forbidden, not_found
from common.security import authenticate
from model.db import ResearchInvite
from model.resp import ListMyInvitations


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


class MyInvites(Resource):
    method_decorators = [authenticate]

    def get(self, current_user):
        my_invites = ResearchInvite.by_email(current_user.email)
        return ListMyInvitations(my_invites).js()


class AcceptMyInvite(Resource):
    method_decorators = [authenticate]

    def post(self, current_user, invite_id):
        invite = ResearchInvite.get(int(invite_id))

        if not invite:
            return not_found('Invite not found.')

        if invite.email != current_user.email:
            return forbidden('It is not your invite.')

        research = invite.research_key.get()

        research.researchers_keys.append(current_user.key)
        research.put()

        invite.key.delete()

        return ok_msg('Invitation accepted.')
