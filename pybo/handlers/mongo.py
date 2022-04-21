from flask import Flask
from flask_mongoengine import MongoEngine
import os
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get("MONGO_INITDB_DATABASE"),
    'host' : os.environ.get("MONGODB_HOST"),
    'port' : int(os.environ.get("MONGODB_PORT")),
    'username' : os.environ.get("MONGO_INITDB_ROOT_USERNAME"),
    'password' : os.environ.get("MONGO_INITDB_ROOT_PASSWORD"),
    'authentication_source' : 'docker_db'
}

class Mongo(object):
    def get_db(self): 
        return MongoEngine(app)