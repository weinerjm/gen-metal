import pymongo, re, random
import nltk
import nltk.data
from pprint import pprint
from nltk.probability import LidstoneProbDist
# grab text from pymongo database

def get_lyrics_text(db, n_records=50):
    cur = db['lyrics'].find().limit(n_records)

    lyrics_list = []
    for album in cur:
        lyrics_dict = album['lyrics']
        for title, lyrics_body in lyrics_dict.iteritems():
            lyrics_clean = re.sub(r'\s+', ' ', lyrics_body).lower().strip()
            lyrics_list.append(lyrics_clean)

    lyrics_text = ' '.join(lyrics_list)

    return lyrics_text

# clean up the descriptions--string parsing stuff
def clean_description(d):
    if d is not None:
        d = re.sub('[.?/(){}!]', ' ',d) # replace punctuation with space
        d = re.sub('[^\w\d\s]','',d) # remove non-alphanumeric and space
        d = re.sub('\s+',' ',d) # replace long spaces with single space
        d = d.lower()
        return d
    else:
        return ''

class TextGen(object):
    def __init__(self, in_text):
        self.est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')

        self.tokenized_text = self.tokenizer.tokenize(in_text)
        self.content_model = nltk.model.ngram.NgramModel(3, self.tokenized_text, estimator=self.est)
        self.text = []

    def random_text(self, n_words=100):
        starting_words = self.content_model.generate(n_words)[-2:]
        content = self.content_model.generate(n_words, starting_words)

        content = ' '.join(content)

        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_tokenizer.tokenize(content) # parse out sentences
        sentences = [sent.capitalize() for sent in sentences]
        #content = ' \n'.join(sentences)
        sentences = map(lambda x: re.sub(r'[\s.]([\',?.!"(](?:\s|$))', r'\1', x), sentences)
        self.text = sentences
        return sentences
