__author__ = 'juan'

import glob
import json
import datetime

hashtag_dict = {}
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

def processTweet(line):
    linea = line
    linea = linea.replace('\\r\\n','')
    linea = linea.replace('\"{', '{')
    linea = linea.replace('}\"', '}')
    linea = linea.decode('unicode_escape')
    linea = linea.lower()
    myjson = json.loads(linea)
    extractHashtags(myjson)

def extractHashtags(myjson):
    global hashtag_dict
    try:
        js2 = myjson['entities']['hashtags']
        for item in js2:
            if(hashtag_dict.get(item['text'],"no_exist") != "no_exist"):
                hashtag_dict[item['text']] = hashtag_dict[item['text']]+1
            else:
                hashtag_dict[item['text']] = 1
    except:
        pass

def printHashtags():
    for v, k in sorted(((v, k) for k, v in hashtag_dict.items()), reverse=True)[0:20]:
        print(k+" - "+str(v))

def loadCorpora():
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        writeLog("Leyendo archivo "+fileDir)
        loadFile(fileDir)

def loadFile(fileDir):
    f = open(fileDir, 'r')
    for line in f:
        if(line.__len__() > 0):
            processTweet(line)


if __name__ == '__main__':
    initLog()
    loadCorpora()
    printHashtags()
    closeLog()
