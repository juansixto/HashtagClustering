__author__ = 'juan'

import glob
import json
import datetime

hashtag_dict = {}
log_file = None
tweet_count = 0
xml_id = 0


def initLog():
    global log_file
    try:
    # This tries to open an existing file but creates a new file if necessary.
        log_file = open("logEnd3.txt", "a")
        #log_file.write('Log Started At : '+str(datetime.datetime.now())+"\n")
    except IOError:
        pass

def closeLog():
    #log_file.write('Log Finished At : '+str(datetime.datetime.now())+"\n")
    log_file.close()

def writeLog(line):
    try:
        log_file.writelines(line +"\n")
    except IOError:
        pass

def processTweet(line):
    global tweet_count
    tweet_count = tweet_count+1

    linea = line
    linea = linea.replace('\\r\\n','')
    linea = linea.replace('\"{', '{')
    linea = linea.replace('}\"', '}')
    linea = linea.decode('unicode_escape')
    linea = linea.lower()
    try:
        myjson = json.loads(linea)
        #extractHashtags(myjson)
        extractRelations(myjson)
        #extractUsers(myjson)
        #extractTime(myjson)
        #extractLocations(myjson)
    except:
        print "Error en linea: "+linea

def extractLocations(myjson):
    global xml_id
    try:
        hashtags = myjson['entities']['hashtags']
        location = myjson['geo']['coordinates']

        if len(hashtags) > 0:
            for hash in hashtags:
                hashtag =  str(hash['text'])
                #line = line +","+ str(location[0])+","+str(location[1])
                writeLog("<node id=\""+str(xml_id)+"\" label=\""+hashtag+"\">")
                writeLog("<attvalue for=\""+"hashtag"+"\" value=\""+hashtag+"\"/>")
                writeLog("<attvalue for=\""+"latitude"+"\" value=\""+str(location[0])+"\"/>")
                writeLog("<attvalue for=\""+"longitude"+"\" value=\""+str(location[1])+"\"/>")
                writeLog("<attvalue for=\""+"time"+"\" value=\""+myjson['created_at'][:13]+"\"/>")
                xml_id = xml_id+1
                writeLog("<attvalues>")
                writeLog("</attvalues>")
                writeLog("</node>")
    except:
        pass


def extractRelations(myjson):
    try:
        hashtags = myjson['entities']['hashtags']
        user = myjson['user']['name']
        if len(hashtags)>1:
                for i,item in enumerate(hashtags):
                    for item2 in hashtags[i+1:]:
                        writeLog(str(item['text'].encode('utf-8', 'ignore')+","+item2['text'].encode('utf-8', 'ignore')))
    except:
        pass

def extractUsers(myjson):
    try:
        hashtags = myjson['entities']['hashtags']
        user = myjson['user']['name']
        for item in hashtags:
            writeLog(str(item['text'].encode('utf-8', 'ignore')+","+user.encode('utf-8', 'ignore')))
    except:
        pass

def extractTime(myjson):
    try:
        hashtags = myjson['entities']['hashtags']
        time = myjson['created_at'][:13]
        for item in hashtags:
            writeLog(str(item['text'].encode('utf-8', 'ignore')+","+time.encode('utf-8', 'ignore')))
    except:
        pass

def extractTimes(myjson):
    pass

def extractHashtags(myjson):
    global hashtag_dict, tweet_count
    try:
        js2 = myjson['entities']['hashtags']
        for item in js2:
            tweet_count = tweet_count + 1
            if(hashtag_dict.get(item['text'],"no_exist") != "no_exist"):
                hashtag_dict[item['text']] = hashtag_dict[item['text']]+1
            else:
                hashtag_dict[item['text']] = 1
    except:
        pass

def printHashtags():
    for v, k in sorted(((v, k) for k, v in hashtag_dict.items()), reverse=True):
        writeLog(str(k.encode('utf-8', 'ignore')+","+str(v).encode('utf-8', 'ignore')))


def loadCorpora():
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        writeLog("Leyendo archivo "+fileDir)
        loadFile(fileDir)

def loadFile(fileDir):
    twcount = 0
    f = open(fileDir, 'r')
    for line in f:
        twcount = twcount+1
        if(line.__len__() > 0 and twcount%1==0):
            processTweet(line)


if __name__ == '__main__':
    initLog()
    loadCorpora()
    closeLog()
    print "================================================="
    print "Terminado con ",tweet_count, " tweets."
    print "================================================="

