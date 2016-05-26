from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
from metalapp import app, mongo
from randgen import get_lyrics_text, TextGen

@app.route("/")
def main():
    lyrics_text = get_lyrics_text(mongo.db, n_records=50)
    tg = TextGen(lyrics_text)
    display_html = ' <br><br>'.join(tg.random_text())
    return display_html

    # the full app
    #return render_template('index.html')

if __name__ == '__main__':
    #app.debug=True
    app.run()
