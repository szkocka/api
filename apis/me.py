from flask.ext.restful import Resource

from common.http_responses import ok, ok_msg, bad_request
from common.insert_wraps import insert_research
from common.security import authenticate
from model.db import ResearchRelationship, RelationshipType
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
        relationships = ResearchRelationship.by_email_and_type(current_user.email, RelationshipType.INVITED)
        researches = map(lambda r: r.research_key.get(), relationships)
        return ListMyInvitations(researches).js()


class AcceptInvite(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, current_user, research):
        relationship = ResearchRelationship.get(research.key, current_user.email)

        if not relationship or relationship.type != RelationshipType.INVITED:
            return bad_request('You not invited.')

        research.researchers_keys.append(current_user.key)
        research.put()

        relationship.type = RelationshipType.ACCEPTED
        relationship.put()

        current_user.researcher_in += 1
        current_user.put()

        return ok_msg('Invitation accepted.')


class RejectInvite(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, current_user, research):
        relationship = ResearchRelationship.get(research.key, current_user.email)

        if not relationship or relationship.type != RelationshipType.INVITED:
            return bad_request('You not invited.')

        relationship.type = RelationshipType.REJECTED
        relationship.put()

        return ok_msg('Invitation rejected.')
