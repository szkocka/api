"""`main` is the top level module for your Flask application."""
from apis.auth import AuthLocalLogin
from apis.pages import UpdateAboutPage, GetAboutPage
from apis.req_to_join import ReqToJoinResearch
from apis.forums import AddMessage, GetForum, ListForums, AddForum
from apis.me import Me
from apis.news import AddNews, ListNews
from apis.researchers import AddResearcher, RemoveResearcher
from apis.researches import AddResearch, UpdateResearch, GetResearch
from apis.researches import ListResearches
from apis.tasks.tasks import ProcessResearchers
from apis.upload import UploadImage
from apis.users import CreateUser, UserDetails, UpdateUser
from flask import Flask
from flask.ext.cors import CORS
from flask.ext.restful import Api

app = Flask(__name__)
CORS(app)
api = Api(app)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


api.add_resource(AddNews, '/news')
api.add_resource(ListNews, '/news')
api.add_resource(AddResearch, '/researches')
api.add_resource(ListResearches, '/researches')
api.add_resource(GetResearch, '/researches/<research_id>')
api.add_resource(UpdateResearch, '/researches/<research_id>')
api.add_resource(GetForum, '/researches/forums/<forum_id>')
api.add_resource(AddMessage, '/researches/forums/<forum_id>')
api.add_resource(ListForums, '/researches/<research_id>/forums')
api.add_resource(AddForum, '/researches/<research_id>/forums')
api.add_resource(AddResearcher, '/researches/<research_id>/invite')
#api.add_resource(AddResearcher, '/researches/<research_id>/researchers')
api.add_resource(RemoveResearcher, '/researches/<research_id>/researchers/<user_id>')
api.add_resource(ReqToJoinResearch, '/researches/<research_id>/join')
api.add_resource(CreateUser, '/users')
api.add_resource(UpdateUser, '/users')
api.add_resource(UserDetails, '/users/<user_id>')
api.add_resource(Me, '/users/me')
api.add_resource(AuthLocalLogin, '/auth/local')
api.add_resource(UploadImage, '/upload')

api.add_resource(UpdateAboutPage, '/pages/about')
api.add_resource(GetAboutPage, '/pages/about')

api.add_resource(ProcessResearchers, '/tasks/process-researchers')
