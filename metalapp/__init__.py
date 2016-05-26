from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
import os
from randgen import get_lyrics_text, TextGen

app = Flask(__name__)
if 'MONGODB_URI' in os.environ.keys():
    MONGODB_URI = os.environ['MONGODB_URI']
else:
    from mongodb_uri import MONGODB_URI

app.config['MONGO_URI'] = MONGODB_URI
app.config['MONGO_DBNAME'] = 'heroku_pzw58gh3' 
mongo = PyMongo(app)

import metalapp.resources
