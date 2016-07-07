"""`main` is the top level module for your Flask application."""
from apis.auth import AuthLocalLogin
from apis.messages import AddMessage, ListMessages
from apis.pages import UpdateAboutPage, GetAboutPage
from apis.queries import FindResearches
from apis.req_to_join import ReqToJoinResearch, ApproveResearcher, RejectResearcher, ListReqToJoinResearch
from apis.forums import GetForum, ListForums, AddForum
from apis.me import Me, MyInvites, AcceptInvite, RejectInvite
from apis.news import AddNews, ListNews
from apis.researchers import InviteResearcher, RemoveResearcher
from apis.researches import AddResearch, UpdateResearch, GetResearch, ListTags
from apis.researches import ListResearches
from apis.tasks.tasks import IndexResearch, NotifyAboutNewMessage
from apis.upload import UploadImage
from apis.users import CreateUser, UserDetails, UpdateUser, ListAllUsers, ListUserResearches, ListUserForums, \
    ListUserMessages, BanUsers, DeleteUsers, UpdatePassword
from flask import Flask
from flask.ext.cors import CORS
from flask.ext.restful import Api

app = Flask(__name__)
CORS(app)
api = Api(app)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


api.add_resource(FindResearches, '/queries/researches')

api.add_resource(AddNews, '/news')
api.add_resource(ListNews, '/news')

api.add_resource(AddResearch, '/researches')
api.add_resource(ListResearches, '/researches')
api.add_resource(GetResearch, '/researches/<research_id>')
api.add_resource(UpdateResearch, '/researches/<research_id>')
api.add_resource(ListTags, '/researches/tags')

api.add_resource(ListForums, '/researches/<research_id>/forums')
api.add_resource(AddForum, '/researches/<research_id>/forums')

api.add_resource(GetForum, '/forums/<forum_id>')
api.add_resource(AddMessage, '/forums/<forum_id>/messages')
api.add_resource(ListMessages, '/forums/<forum_id>/messages')

api.add_resource(InviteResearcher, '/researches/<research_id>/invites')
api.add_resource(RemoveResearcher, '/researches/<research_id>/researchers/<user_id>')
api.add_resource(ApproveResearcher, '/researches/<research_id>/researchers/<user_id>/approved')
api.add_resource(RejectResearcher, '/researches/<research_id>/researchers/<user_id>/rejected')
api.add_resource(ReqToJoinResearch, '/researches/<research_id>/requests')
api.add_resource(ListReqToJoinResearch, '/researches/<research_id>/requests')

api.add_resource(BanUsers, '/users/banned')
api.add_resource(DeleteUsers, '/users/deleted')
api.add_resource(CreateUser, '/users')
api.add_resource(UpdateUser, '/users')
api.add_resource(ListAllUsers, '/users')
api.add_resource(UserDetails, '/users/<user_id>')
api.add_resource(ListUserResearches, '/users/<user_id>/researches')
api.add_resource(ListUserForums, '/users/<user_id>/forums')
api.add_resource(ListUserMessages, '/users/<user_id>/messages')
api.add_resource(Me, '/users/me')
api.add_resource(UpdatePassword, '/users/me/password')
api.add_resource(MyInvites, '/users/me/invites/researches')
api.add_resource(AcceptInvite, '/users/me/invites/researches/<research_id>/accepted')
api.add_resource(RejectInvite, '/users/me/invites/researches/<research_id>/declined')

api.add_resource(AuthLocalLogin, '/auth/local')
api.add_resource(UploadImage, '/upload')

api.add_resource(UpdateAboutPage, '/pages/about')
api.add_resource(GetAboutPage, '/pages/about')

api.add_resource(IndexResearch, '/tasks/index-research')
api.add_resource(NotifyAboutNewMessage, '/tasks/notify-new-message')
