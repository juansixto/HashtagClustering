__author__ = 'juan'
import datetime
import glob
import json

log_file = None
tweet_count = 0
hashtag_dict = {}
fileLog = ""

# LOG PROCESS ==========================================================================================

def initLog():
    global log_file
    try:
    # This tries to open an existing file but creates a new file if necessary.
        name = "Log_"+fileLog[26:]
        print name
        log_file = open(name, "a")
        #log_file.write('Log Started At : '+str(datetime.datetime.now())+"\n")
    except IOError:
        pass

def writeLog(line):
    try:
        log_file.writelines(line +"\n")
    except IOError:
        pass

def saveDict(dictionary):
    for v, k in sorted(((v, k) for k, v in dictionary.items()), reverse=True):
        try:
            writeLog(str(k.encode('utf-8', 'ignore')+" : "+str(v).encode('utf-8', 'ignore')))
        except:
            print "Error printing: ", k, " + " , v

def closeLog():
    log_file.write('Log Finished At : '+str(datetime.datetime.now())+"\n")
    log_file.close()


# END LOG PROCESS =======================================================================================
# CORPORA PROCESS =======================================================================================
def loadCorpora():
    global hashtag_dict, fileLog
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        fileLog = fileDir
        initLog()
        writeLog("Leyendo archivo "+fileDir)
        loadFile(fileDir)
        closeLog()
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
        extractRelations(myjson)
    except:
        pass


# END CORPORA PROCESS ==================================================================================
# TWEET PROCESS ========================================================================================

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

# END TWEET PROCESS ====================================================================================
# MAIN PROCESS =========================================================================================
if __name__ == '__main__':
    loadCorpora()