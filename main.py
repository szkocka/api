"""`main` is the top level module for your Flask application."""
from flask import Flask
from flask.ext.cors import CORS
from flask.ext.restful import Api
from db.model import db
from init import add_resources

app = Flask(__name__)

config = app.config
config.from_pyfile('app.properties')

db.init_app(app)

CORS(app)
api = Api(app)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

add_resources(api)
