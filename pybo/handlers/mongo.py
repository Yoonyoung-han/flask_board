from flask import Flask
from flask_mongoengine import MongoEngine
import config

app = Flask(__name__)
app.config['MONGODB_DB'] = config.DATABASE
app.config['MONGODB_HOST'] = config.HOST
app.config['MONGODB_PORT'] = config.PORT
app.config['MONGODB_USERNAME'] = config.USER
app.config['MONGODB_PASSWORD'] = config.PASSWORD

class Mongo(object):
    def get_db(self):
        return MongoEngine(app)