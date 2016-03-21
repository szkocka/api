"""`main` is the top level module for your Flask application."""
from apis.auth import AuthLocalLogin
from apis.req_to_join import ReqToJoinResearch
from apis.invite_to_join import InviteToJoinResearch
from apis.forums import AddMessage, GetForum, ListForums, AddForum
from apis.me import Me
from apis.news import AddNews, ListNews
from apis.researches import AddResearch, UpdateResearch, GetResearch
from apis.researches import ListResearches
from apis.tasks.tasks import ProcessResearchers
from apis.upload import Upload
from apis.users import CreateUser
from flask import Flask
from flask.ext.cors import CORS
from flask.ext.restful import Api

app = Flask(__name__)

config = app.config
config.from_pyfile('app.properties')


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
api.add_resource(InviteToJoinResearch, '/researches/<research_id>/invite')
api.add_resource(ReqToJoinResearch, '/researches/<research_id>/join')
api.add_resource(CreateUser, '/users')
api.add_resource(AuthLocalLogin, '/auth/local')
api.add_resource(Me, '/users/me')
api.add_resource(Upload, '/upload')

api.add_resource(ProcessResearchers, '/tasks/process-researchers')
