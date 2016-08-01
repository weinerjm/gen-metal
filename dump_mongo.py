import pymongo, gzip
from bson import Binary, Code, json_util

def main():
    #dump_lyrics_db()
    
    TRY_LOAD = True
    if TRY_LOAD:
        lyrics_to_text(title_only=False)

def lyrics_to_text(title_only=False):
    fname = 'lyrics.json.gz'
    
    print "reading in file {0}".format(fname)
    albums = load_file(fname)
    outf = 'titles.txt' if title_only else 'all_lyrics.txt'
    with open(outf, 'w') as fout:
        for album in albums:
            for title, lyrics in album['lyrics'].iteritems():
                if title_only:
                    out_str = title.encode('utf-8')
                    out_str = out_str.replace(',','.') + '\n'
                else:
                    out_str = lyrics.encode('utf-8') + "\n--END--"
                fout.write(out_str)


def dump_lyrics_db():
    client = pymongo.MongoClient()
    db = client['lyricsdb']
    records = db['lyrics'].find()

    fname = 'lyrics.json.gz'
    with gzip.open(fname, 'wb') as outfile:
        outfile.write(json_util.dumps(list(records), outfile,
                       indent=4,
                       default=json_util.default))
    outfile.close()
    print "done!"

def load_file(name):
    with gzip.open(name, 'rb') as infile:
        return json_util.loads(infile.read())

if __name__ == '__main__':
    main()
