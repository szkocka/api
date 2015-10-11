from flask import Flask
from flask.ext.cors import CORS
from flask.ext.restful import Api
from db.model import sql

from db.util import DB

app = Flask(__name__)

app.config.from_object('config')
sql.init_app(app)

db = DB(sql)
CORS(app)
api = Api(app)
