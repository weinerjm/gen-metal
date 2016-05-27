from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
import os
from .randgen import get_lyrics_text, TextGen

app = Flask(__name__, instance_relative_config=True)
# Load the default config
app.config.from_object('config.default')


# use heroku environment variables
if 'MONGODB_URI' in os.environ:
    app.config['MONGO_URI'] = os.environ['MONGODB_URI']
    app.config['MONGO_DBNAME'] = os.environ['MONGODB_URI'].split('/')[-1]
else:
    # Load configuration from instance folder
    app.config.from_pyfile('config.py')
    app.debug = True

mongo = PyMongo(app)

import resources
