__author__ = 'juan'

import glob
import json
import unicodedata

hashtag_dict = {}
tweet_dict = []
hashtag_relations = []

def loadCorpora():
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        print "Leyendo archivo "+fileDir
        loadFile(fileDir)

def loadFile(fileDir):
    global tweet_dict
    f = open(fileDir)
    for linea in f:
        linea = linea.replace('\\r\\n','')
        linea = linea.replace('\"{', '{')
        linea = linea.replace('}\"', '}')
        linea = linea.decode('unicode_escape')
        linea = linea.lower()
        myjson = json.loads(linea)
        tweet_dict.append(myjson)
        js2 = myjson['entities']['hashtags']
        for item in js2:
            if(hashtag_dict.get(item['text'],"no_exist") != "no_exist"):
                hashtag_dict[item['text']] = hashtag_dict[item['text']]+1
            else:
                hashtag_dict[item['text']] = 1
    for v, k in sorted(((v, k) for k, v in hashtag_dict.items()), reverse=True)[0:30]:
        print k+" - "+str(v)
    f.close()

def extractRelations(item):
    cross_dict =  {}
    print "======================"
    print "Extract from: ",item
    print "======================"
    for tweet in tweet_dict:
        hashtags = tweet['entities']['hashtags']
        hashlist = []
        if len(hashtags)>1:
            hashtag_relations.append(hashtags)
            if  item in str(hashtags):
                print hashtags
                for h in hashtags:
                    hashlist.append(h['text'])
                    if item in str(hashtags):
                        if(cross_dict.get(h['text'],"no_exist") != "no_exist"):
                            cross_dict[h['text']] = cross_dict[h['text']]+1

                        else:
                            cross_dict[h['text']] = 1
    for v, k in sorted(((v, k) for k, v in cross_dict.items()), reverse=True):
        print k+" - "+str(v)
if __name__ == '__main__':
   loadCorpora()
   extractRelations("shutdown")
   print "================================================="
   print "Terminado con ",tweet_dict.__len__() , " tweets."
   print "================================================="
