from flask import Flask, render_template
#from flask.ext.pymongo import PyMongo
import pymongo, os
from randgen import get_lyrics_text, TextGen
app = Flask(__name__)
#mongo = PyMongo(app)
import sys
sys.setdefaultencoding("utf-8")

@app.route("/")
def main():
    if 'MONGODB_URI' not in os.environ.keys():
        from mongodb_uri import MONGODB_URI
        client = pymongo.MongoClient(MONGODB_URI,
                                     connectTimeoutMS=30000,
                                     socketTimeoutMS=None,
                                     socketKeepAlive=True)
    else:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'],
                                     connectTimeoutMS=30000,
                                     socketTimeoutMS=None,
                                     socketKeepAlive=True)
    
    db = client.get_default_database()
    lyrics_text = get_lyrics_text(db, n_records=20)
    return lyrics_text
    #tg = TextGen(lyrics_text)
    #display_html = ' \n'.join(tg.random_text())
    #return display_html

    # the full app
    #return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

if __name__ == '__main__':
    #app.debug=True
    app.run()
