__author__ = 'juan'
import datetime
import glob
import json

log_file = None
tweet_count = 0
hashtag_dict = {}

# LOG PROCESS ==========================================================================================

def initLog():
    global log_file
    try:
    # This tries to open an existing file but creates a new file if necessary.
        log_file = open("HashtagMetrics.txt", "a")
        log_file.write('Log Started At : '+str(datetime.datetime.now())+"\n")
    except IOError:
        pass

def writeLog(line):
    try:
        log_file.writelines(line +"\n")
    except IOError:
        pass

def saveDict(dictionary):
    print hashtag_dict
    for v, k in sorted(((v, k) for k, v in dictionary.items()), reverse=True):
        writeLog(str(k.encode('utf-8', 'ignore')+" : "+str(v).encode('utf-8', 'ignore')))

def closeLog():
    log_file.write('Log Finished At : '+str(datetime.datetime.now())+"\n")
    log_file.close()


# END LOG PROCESS =======================================================================================
# CORPORA PROCESS =======================================================================================
def loadCorpora():
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        print("Leyendo archivo "+fileDir)
        writeLog("Leyendo archivo "+fileDir)
        loadFile(fileDir)

def loadFile(fileDir):
    global hashtag_dict
    twcount = 0
    f = open(fileDir, 'r')
    for line in f:
        twcount = twcount+1
        if(line.__len__() > 0):
            processTweet(line)
    saveDict(hashtag_dict)

def processTweet(line):
    linea = line
    linea = linea.replace('\\r\\n','')
    linea = linea.replace('\"{', '{')
    linea = linea.replace('}\"', '}')
    linea = linea.decode('unicode_escape')
    linea = linea.lower()
    try:
        myjson = json.loads(linea)
        extractHashtags(myjson)
    except:
        pass


# END CORPORA PROCESS ==================================================================================
# TWEET PROCESS ========================================================================================

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
# END TWEET PROCESS ====================================================================================
# MAIN PROCESS =========================================================================================
if __name__ == '__main__':
    initLog()
    loadCorpora()
    closeLog()