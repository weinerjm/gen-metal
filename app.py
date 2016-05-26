from flask import Flask, render_template
#from flask.ext.pymongo import PyMongo
import pymongo, os
from randgen import get_lyrics_text, TextGen
app = Flask(__name__)
#mongo = PyMongo(app)


@app.route("/")
def main():
    if 'MONGODB_URI' in os.environ.keys():
        client = pymongo.MongoClient(os.environ['MONGODB_URI'],
                                     connectTimeoutMS=30000,
                                     socketTimeoutMS=None,
                                     socketKeepAlive=True)
    else:
        from mongodb_uri import MONGODB_URI
        client = pymongo.MongoClient(MONGODB_URI,
                                     connectTimeoutMS=30000,
                                     socketTimeoutMS=None,
                                     socketKeepAlive=True)
     
    db = client.get_default_database()
    lyrics_text = get_lyrics_text(db, n_records=20)
    tg = TextGen(lyrics_text)
    display_html = ' \n'.join(tg.random_text())
    return display_html

    # the full app
    #return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
