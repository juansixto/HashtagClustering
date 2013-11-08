__author__ = 'juan'
import datetime
import glob
import json
import sys

log_file = None
tweet_count = 0
hashtag_dict = {}
hashtag_filter = "shutdown"

# LOG PROCESS ==========================================================================================

def initLog():
    global log_file
    try:
    # This tries to open an existing file but creates a new file if necessary.
        log_title = "HashtagTimeFreq"+hashtag_filter+".txt"
        log_file = open(log_title, "a")
        log_file.write('Log Started At : '+str(datetime.datetime.now())+"\n")
    except IOError:
        pass

def writeLog(line):
    try:
        log_file.writelines(line +"\n")
    except IOError:
        pass

def saveDict(dictionary):
    for v, k in sorted(((v, k) for k, v in dictionary.items()), reverse=True):
        writeLog(str(k.encode('utf-8', 'ignore')+" : "+str(v).encode('utf-8', 'ignore')))

def closeLog():
    log_file.write('Log Finished At : '+str(datetime.datetime.now())+"\n")
    log_file.close()


# END LOG PROCESS =======================================================================================
# CORPORA PROCESS =======================================================================================
def loadCorpora():
    global hashtag_dict
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        writeLog("Leyendo archivo "+fileDir)
        loadFile(fileDir)
    saveDict(hashtag_dict)

def loadFile(fileDir):
    twcount = 0
    f = open(fileDir, 'r')
    for line in f:
        twcount = twcount+1
        if(line.__len__() > 0):
            processTweet(line)


def processTweet(line):
    linea = line
    linea = linea.replace('\\r\\n','')
    linea = linea.replace('\"{', '{')
    linea = linea.replace('}\"', '}')
    linea = linea.decode('unicode_escape')
    linea = linea.lower()
    try:
        myjson = json.loads(linea)
        hashtags = myjson['entities']['hashtags']
        isHashtag = False
        for item in hashtags:
            if item['text'] == hashtag_filter:
                isHashtag = True
        if isHashtag:
            print hashtags
            extractTimes(myjson)
    except:
        pass


# END CORPORA PROCESS ==================================================================================
# TWEET PROCESS ========================================================================================

def extractTimes(myjson):
    global hashtag_dict
    try:
        js2 = myjson['created_at'][:13]
        if(hashtag_dict.get(js2,"no_exist") != "no_exist"):
            hashtag_dict[js2] = hashtag_dict[js2]+1
        else:
            hashtag_dict[js2] = 1
    except:
        pass

# END TWEET PROCESS ====================================================================================
# MAIN PROCESS =========================================================================================
if __name__ == '__main__':
    hashtag_filter = sys.argv[1]
    initLog()
    loadCorpora()
    closeLog()