from flask import request
from flask.ext.restful import Resource

from common.http_responses import ok_msg, ok, bad_request
from common.insert_wraps import insert_research, insert_user
from common.security import authenticate, is_supervisor
from emails import sender
from emails.views import ReqToJoinSubj, ReqToJoin
from model.db import ResearchRelationship, RelationshipType, User
from model.resp import ListReqToJoin


class ReqToJoinResearch(Resource):
    method_decorators = [insert_research, authenticate]

    def post(self, research, current_user):
        if self.__relationship_exists(research, current_user.email):
            return bad_request('Already requested.')
        self.__add_relationship(research, current_user.email)

        supervisor = research.supervisor_key.get()
        user_name = current_user.name

        recipient = supervisor.email
        supervisor_name = supervisor.name

        title = research.title
        text = request.json.get('text', '')

        subj_view = ReqToJoinSubj(user_name, title)
        body_view = ReqToJoin(user_name, title, supervisor_name, text)
        sender.send_email(subj_view, body_view, recipient)

        return ok_msg('Request was send to research supervisor.')

    def __relationship_exists(self, research, recipient):
        return ResearchRelationship.get(research.key, recipient)

    def __add_relationship(self, research, recipient):
        ResearchRelationship(research_key=research.key,
                             user_email=recipient,
                             type=RelationshipType.WANTS_TO_JOIN).put()


class ApproveResearcher(Resource):
    method_decorators = [is_supervisor, insert_user, insert_research, authenticate]

    def post(self, research, user, current_user):
        relationship = ResearchRelationship.get(research.key, user.email)

        if not relationship or relationship.type != RelationshipType.WANTS_TO_JOIN:
            return bad_request('User don\'t want to join.')

        research.researchers_keys.append(user.key)
        research.put()

        relationship.type = RelationshipType.APPROVED
        relationship.put()

        user.researcher_in += 1
        user.put()

        return ok_msg('Researcher accepted.')


class RejectResearcher(Resource):
    method_decorators = [is_supervisor, insert_user, insert_research, authenticate]

    def post(self, research, user, current_user):
        relationship = ResearchRelationship.get(research.key, user.email)

        if not relationship or relationship.type != RelationshipType.WANTS_TO_JOIN:
            return bad_request('User don\'t want to join.')

        relationship.type = RelationshipType.REJECTED
        relationship.put()

        return ok_msg('Researcher rejected.')


class ListReqToJoinResearch(Resource):
    method_decorators = [is_supervisor, insert_research, authenticate]

    def get(self, research, current_user):
        relationships = ResearchRelationship.by_research_and_type(research.key, RelationshipType.WANTS_TO_JOIN)
        users = map(lambda r: User.by_email(r.user_email), relationships)

        return ok(ListReqToJoin(users).js())
