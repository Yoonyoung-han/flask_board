from flask import Flask
from flask_mongoengine import MongoEngine
import os
# from dotenv import load_dotenv

# load_dotenv('config.env')

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get("DATABASE"),
    'host' : os.environ.get("HOST"),
    'port' : int(os.environ.get("PORT")),
    # 'username' : os.environ.get("MONGODB_USERNAME"),
    # 'password' : os.environ.get("PASSWORD"),
    'authentication_source' : 'admin'
}

class Mongo(object):
    def get_db(self):
        return MongoEngine(app)