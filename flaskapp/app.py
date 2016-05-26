from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
import pymongo
import os
app = Flask(__name__)
mongo = PyMongo(app)

@app.route("/")
def main():
    client = pymongo.MongoClient(os.environ['MONGODB_URI'])
    db = client.get_default_database()
    res = db['lyrics'].find_one()
    return str(res)
    #return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()
