from flask import Flask
from pymongo import MongoClient
from flask.ext.restful import Api
from resources.auth import AuthLocal
from resources.forum import Forum
from resources.forums import Forums
from resources.me import Me
from resources.researches import Researches
from resources.news import News
from resources.research import Research
from resources.users import Users

app = Flask(__name__)
api = Api(app)

mongo_client = MongoClient('mongodb://localhost:27017/')

resource_args = {'db': mongo_client.lsm, 'logger': app.logger}

api.add_resource(News, '/news', resource_class_kwargs=resource_args)
api.add_resource(Researches, '/researches', resource_class_kwargs=resource_args)
api.add_resource(Research, '/researches/<research_id>', resource_class_kwargs=resource_args)
api.add_resource(Forum, '/researches/forums/<forum_id>', resource_class_kwargs=resource_args)
api.add_resource(Forums, '/researches/<research_id>/forums', resource_class_kwargs=resource_args)
api.add_resource(AuthLocal, '/auth/local', resource_class_kwargs=resource_args)
api.add_resource(Me, '/users/me', resource_class_kwargs=resource_args)
api.add_resource(Users, '/users', resource_class_kwargs=resource_args)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
