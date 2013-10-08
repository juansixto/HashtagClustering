__author__ = 'juan'

import glob
import json
import datetime

hashtag_dict = {}
tweet_dict = []
hashtag_relations = []
log_file = None

def initLog():
    global log_file
    try:
    # This tries to open an existing file but creates a new file if necessary.
        log_file = open("log.txt", "a")
        log_file.write('Log Started At : '+str(datetime.datetime.now())+"\n")
    except IOError:
        pass

def closeLog():
    log_file.write('Log Finished At : '+str(datetime.datetime.now())+"\n")
    log_file.close()

def writeLog(line):
    try:
        log_file.writelines(line +"\n")
    except IOError:
        pass


def loadCorpora():
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        writeLog("Leyendo archivo "+fileDir)
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
    for v, k in sorted(((v, k) for k, v in hashtag_dict.items()), reverse=True)[0:20]:
        writeLog(k+" - "+str(v))
    f.close()

def extractLocations(item):
    print "======================"
    print "Locations from: ",item
    print "======================"
    for tweet in tweet_dict:
        hashtags = str(tweet['entities']['hashtags'])
        if item in hashtags:
            location = tweet['user']['geo_enabled']
            if (str(location) != "False"):
                writeLog(tweet['geo'])

def extractRelations(item):
    cross_dict =  {}
    writeLog("======================")
    writeLog("Relations from: "+item)
    writeLog("======================")
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
    for v, k in sorted(((v, k) for k, v in cross_dict.items()), reverse=True)[:20]:
        writeLog(((k)+" - "+str(v)).encode('utf-8', 'ignore'))

def extractUsers(item):
    users_dict =  {}
    total_tweets = 0
    print "======================"
    print "Users from: ",item
    print "======================"
    for tweet in tweet_dict:
        if(len(tweet['entities']['hashtags'])>0):
            if(users_dict.get(tweet['user']['name'],"no_exist") != "no_exist"):
                users_dict[tweet['user']['name']] = users_dict[tweet['user']['name']]+1
            else:
                users_dict[tweet['user']['name']] = 1
    for v, k in sorted(((v, k) for k, v in users_dict.items()), reverse=True):
        total_tweets = total_tweets + v
        print k+" - "+str(v)

def extractTimes(list):
    writeLog("======================")
    writeLog("Time List")
    writeLog("======================")
    times_dict = {}
    for tweet in list:
        time = tweet['created_at'][:13]
        if(times_dict.get(time,"no_exist") != "no_exist"):
            times_dict[time] = times_dict[time]+1
        else:
                times_dict[time] = 1
    for v, k in sorted(((k, v) for k, v in times_dict.items()), reverse=False):
        writeLog((v+" - "+str(k)).encode('utf-8', 'ignore'))

if __name__ == '__main__':
    initLog()
    loadCorpora()
    extractRelations("shutdown")
    extractTimes(tweet_dict)
    closeLog()
    print "================================================="
    print "Terminado con ",tweet_dict.__len__() , " tweets."
    print "================================================="
