import pymongo, gzip, os
from bson import Binary, Code, json_util

def main():
    mongolab_uri = os.environ['MONGODB_URI']

    client = pymongo.MongoClient(mongolab_uri,
                                 connectTimeoutMS=30000,
                                 socketTimeoutMS=None,
                                 socketKeepAlive=True)
    out_db = client.get_default_database()
    out_coll = 'lyrics'

    fname = 'lyrics.json.gz'
    in_lyrics = load_file(fname)

    print "updating lyrics db..."
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
