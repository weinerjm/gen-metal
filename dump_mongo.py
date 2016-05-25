import pymongo, gzip
from bson import Binary, Code, json_util

def main():
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

    TRY_LOAD = False
    if TRY_LOAD:
        print "reading in file {0}".format(fname)
        res = load_file(fname)
        print res
        

def load_file(name):
    with gzip.open(name, 'rb') as infile:
        return json_util.loads(infile.read())

if __name__ == '__main__':
    main()
