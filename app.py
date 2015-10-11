from flask import Flask
from flask.ext.cors import CORS
from flask.ext.restful import Api
from db.model import db

app = Flask(__name__)

app.config.from_object('config')
db.init_app(app)

CORS(app)
api = Api(app)
