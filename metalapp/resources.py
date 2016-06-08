from flask import Flask, request, render_template, current_app, url_for
from flask.ext.pymongo import PyMongo
from metalapp import app, mongo
from randgen import get_lyrics_text, TextGen
from fix_unicode import fix_bad_unicode
import ftfy

with app.app_context():
    categories = ['all','judas_priest','highlander',
                  'violence','blasphemy','spooky']

    lyrics_build = get_lyrics_text(mongo.db, n_records=100, sort_field=None)
    tg_dict = {}
    tg_dict['all'] = TextGen(lyrics_build)

@app.route("/")
def main():
    global tg_dict
    #display_html = map(lambda x: ftfy.fix_text(x, fix_entities=False), tg_dict['all'].random_text())
    display_html = tg_dict['all'].random_text()
    try:
        pass
        #display_html = fix_bad_unicode(' '.join(display_html).decode('latin9').encode('utf8'))
    except:
        display_html.append(u"unicode failed")

    # want to render here
    return render_template('index.html', category='All', text_lines=display_html)

@app.route('/<category>', defaults={'n': 100})
@app.route('/<category>/<int:n>')
def special_lyrics(category, n):
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
        lyrics_text = get_lyrics_text(mongo.db, n_records=n, 
                                      sort_field=(category,6))
        tg_dict[category] = TextGen(lyrics_text)
    
    #display_html = map(lambda x: ftfy.fix_text(x, fix_entities=False), tg_dict[category].random_text())
    display_html = tg_dict['all'].random_text()
    try:
        pass
        #display_html = fix_bad_unicode(' '.join(display_html).decode('latin9').encode('utf8'))
    except:
        display_html.append(u"unicode failed")

    # want to render here
    return render_template('index.html', category=category.title(), text_lines=display_html)

if __name__ == '__main__':
    #app.debug=True
    app.run()
