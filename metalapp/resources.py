from flask import Flask, render_template, current_app
from flask.ext.pymongo import PyMongo
from metalapp import app, mongo
from randgen import get_lyrics_text, TextGen

with app.app_context():
    categories = ['all','judas_priest','highlander',
                  'violence','blasphemy','spooky']

    lyrics_build = get_lyrics_text(mongo.db, n_records=50, sort_field=None)
    tg_dict = {}
    tg_dict['all'] = TextGen(lyrics_build)

@app.route("/")
def main():
    global tg_dict
    #TODO: make all display_html templates
    display_html = '<center><h1>All Lyrics</h1></center>'
    display_html += '<br><br>'.join(tg_dict['all'].random_text())
    return display_html

    # want to render here
    #return render_template('index.html')

@app.route('/<category>')
def special_lyrics(category):
    """
    Given a category, generate random lyrics for that category.
    If a TextGen object doesn't exist for that category, fetch the data
    and create one.

    Return formatted lyrics text
    """
    global tg_dict
    if category not in categories:
        return "invalid category: {0}".format(category)
    # make  
    if category not in tg_dict:
        lyrics_text = get_lyrics_text(mongo.db, n_records=50, 
                                      sort_field=(category,0.2))
        tg_dict[category] = TextGen(lyrics_text)
    
    #TODO: make all display_html templates
    display_html = '<center><h1>{0} Lyrics</h1></center>'.format(category.title())
    display_html += '<br><br>'.join(tg_dict[category].random_text())
    
    return display_html

if __name__ == '__main__':
    #app.debug=True
    app.run()
