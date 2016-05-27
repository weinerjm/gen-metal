import pymongo, re, random, string
import nltk
import nltk.data
nltk.data.path.append('./nltk_data/')
from pprint import pprint
from nltk.probability import LidstoneProbDist
from fix_unicode import fix_bad_unicode

def get_lyrics_text(db, n_records=50, sort_field=None):
    """
    Gets raw lyrics text from Mongo database.
    """
    if sort_field:
        field, cutoff = sort_field
        cur = db['lyrics'].find({field: {'$gt': cutoff}}).limit(n_records)
    else:
        cur = db['lyrics'].find().limit(n_records)
    
    
    lyrics_list = []
    
    for album in cur:
        lyrics_dict = album['lyrics']
        for title, lyrics_body in lyrics_dict.iteritems():
            #lyrics_clean = re.sub(r'\s+', ' ', lyrics_body).lower().strip()
            lyrics_clean = lyrics_body
            lyrics_list.append(lyrics_clean)
    
    lyrics_text = u' '.join(lyrics_list)

    return lyrics_text

class TextGen(object):
    def __init__(self, in_text):
        self.est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')

        self.tokenized_text = self.tokenizer.tokenize(in_text)
        self.content_model = nltk.model.ngram.NgramModel(3, self.tokenized_text, estimator=self.est)
        self.text = ''

    def random_text(self, n_words=100):
        starting_words = self.content_model.generate(n_words)[-2:]
        while starting_words[0] in string.punctuation:
            starting_words = self.content_model.generate(n_words)[-2:]
        
        content = self.content_model.generate(n_words, starting_words)

        content = u' '.join(content)

        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_tokenizer.tokenize(content) # parse out sentences
        sentences = [sent.capitalize() for sent in sentences]
        #content = ' \n'.join(sentences)
        sentences = map(lambda x: re.sub(r'[\s.]([\',?.!"(](?:\s|$))', r'\1', x), sentences)
        sentences = map(lambda x: re.sub(r"i'\s+", r"I'", x), sentences)
        sentences = map(lambda x: re.sub(r"'\s+", "'", x), sentences)
        sentences = map(lambda x: re.sub(r"\s+i\s+", " I ", x), sentences)
        self.text = sentences # save the text
        return sentences
