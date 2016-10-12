from flask.ext.restful import Resource
from flask import request
from common.http_responses import ok_msg, bad_request, not_found
from common.insert_wraps import insert_research, insert_user
from common.security import is_supervisor, authenticate, is_admin
from common.validation import validate_request
from model.db import ResearchRelationship, RelationshipType, User
from emails import sender
from emails.views import InviteToJoinSubj, InviteToJoin


class RemoveResearcher(Resource):
    method_decorators = [is_supervisor, insert_research, insert_user, authenticate]

    def delete(self, current_user, research, user):
        self.__delete_relationship(research, user)
        self.__delete_researcher(research, user)

        return ok_msg('Researcher removed from research.')

    def __delete_researcher(self, research, user):
        research.researchers_keys.remove(user.key)
        research.put()

    def __delete_relationship(self, research, user):
        relationship = ResearchRelationship.get(research.key, user.email)
        relationship.key.delete()


class InviteResearcher(Resource):
    method_decorators = [is_supervisor, insert_research, validate_request, authenticate]
    required_fields = ['email', 'name']  # used by validate_request

    def post(self, research, current_user):
        recipient = request.json['email']
        name = request.json['name']
        text = request.json.get('text', '')

        if self.__relationship_exists(research, recipient):
            return bad_request('Already invited.')
        self.__add_relationship(research, recipient)

        supervisor = current_user.name
        title = research.title
        description = research.brief_desc

        subj_view = InviteToJoinSubj(supervisor, title)
        body_view = InviteToJoin(supervisor, title, description, name, text)
        sender.send_email(subj_view, body_view, recipient)

        return ok_msg("Invitation send to {0}".format(recipient))

    def __relationship_exists(self, research, recipient):
        return ResearchRelationship.get(research.key, recipient)

    def __add_relationship(self, research, recipient):
        ResearchRelationship(research_key=research.key,
                             user_email=recipient,
                             type=RelationshipType.INVITED).put()


class UpdateSupervisor(Resource):
    method_decorators = [is_admin, insert_research, validate_request, authenticate]
    required_fields = ['new_supervisor']

    def put(self, current_user, research):
        new_supervisor_email = request.json['new_supervisor']
        supervisor = User.by_email(new_supervisor_email)

        if not supervisor:
            return not_found('User with email not found.')

        self.__delete_relationship(research, research.supervisor_key.get())
        research.supervisor_key = supervisor.key
        research.put()
        self.__add_relationship(research.key, supervisor)

        return ok_msg('Supervisor is updated.')

    def __delete_relationship(self, research, user):
        relationship = ResearchRelationship.get(research.key, user.email)
        relationship.key.delete()

    def __add_relationship(self, research_key, user):
        ResearchRelationship(research_key=research_key,
                         user_email=user.email,
                         type=RelationshipType.SUPERVISOR).put()


class AddResearcher(Resource):
    method_decorators = [is_admin, insert_research, validate_request, authenticate]
    required_fields = ['new_researcher']

    def post(self, current_user, research):
        researcher_email = request.json['new_researcher']
        researcher = User.by_email(researcher_email)

        if not researcher:
            return not_found('User with email not found.')

        if researcher.key in research.researchers_keys \
                or research.supervisor_key == researcher.key:
            return bad_request('User already is researcher.')

        research.researchers_keys.append(researcher.key)
        research.put()

        self.__add_relationship(research.key, researcher_email)

        return ok_msg('Researcher is added.')

    def __add_relationship(self, research_key, email):
        ResearchRelationship(research_key=research_key,
                             user_email=email,
                             type=RelationshipType.ADDED_BY_ADMIN).put()
