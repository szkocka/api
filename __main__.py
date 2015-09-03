from flask import Flask
from flask.ext.cors import CORS
from pymongo import MongoClient
from flask.ext.restful import Api
from mailer.mailer import Mailer

from resources.auth import AuthLocalLogin
from resources.forums import ListForums, AddForum, GetForum, AddMessage
from resources.me import Me
from resources.news import AddNews, ListNews
from resources.researches import AddResearch, ListResearches, GetResearch, UpdateResearch, InviteToJoinResearch, \
    ReqToJoinResearch
from resources.upload import Upload
from resources.users import CreateUser

app = Flask(__name__)
api = Api(app)
CORS(app)

mongo_client = MongoClient('mongodb://localhost:27017/')
mailer = Mailer()

resource_args = {
    'db': mongo_client.lsm,
    'logger': app.logger,
    'mailer': mailer
}

api.add_resource(AddNews, '/news', resource_class_kwargs=resource_args)
api.add_resource(ListNews, '/news', resource_class_kwargs=resource_args)
api.add_resource(AddResearch, '/researches', resource_class_kwargs=resource_args)
api.add_resource(ListResearches, '/researches', resource_class_kwargs=resource_args)
api.add_resource(GetResearch, '/researches/<research_id>', resource_class_kwargs=resource_args)
api.add_resource(UpdateResearch, '/researches/<research_id>', resource_class_kwargs=resource_args)
api.add_resource(GetForum, '/researches/forums/<forum_id>', resource_class_kwargs=resource_args)
api.add_resource(AddMessage, '/researches/forums/<forum_id>', resource_class_kwargs=resource_args)
api.add_resource(ListForums, '/researches/<research_id>/forums', resource_class_kwargs=resource_args)
api.add_resource(AddForum, '/researches/<research_id>/forums', resource_class_kwargs=resource_args)
api.add_resource(InviteToJoinResearch, '/researches/<research_id>/invite', resource_class_kwargs=resource_args)
api.add_resource(ReqToJoinResearch, '/researches/<research_id>/join', resource_class_kwargs=resource_args)
api.add_resource(CreateUser, '/users', resource_class_kwargs=resource_args)
api.add_resource(AuthLocalLogin, '/auth/local', resource_class_kwargs=resource_args)
api.add_resource(Me, '/users/me', resource_class_kwargs=resource_args)
api.add_resource(Upload, '/upload', resource_class_kwargs=resource_args)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
