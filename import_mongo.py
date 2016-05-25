import pymongo, gzip, os
from bson import Binary, Code, json_util

def main():
    client = pymongo.MongoClient()

    out_db = client['lyricsdb-copy']
    out_coll = 'lyrics'

    fname = 'lyrics.json.gz'
    in_lyrics = load_file(fname)

    for album in in_lyrics:
        out_db[out_coll].update_one({'_id': album['_id']},
                                    {'$set': album},
                                    upsert=True)
    
    print "done!"

def load_file(name):
    with gzip.open(name, 'rb') as infile:
        return json_util.loads(infile.read())

if __name__ == '__main__':
    main()
