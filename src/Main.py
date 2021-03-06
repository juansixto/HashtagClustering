'''
Created on 25/09/2013

@author: juan
'''

import glob
import xlrd
import json

corpora = []
hashtag_dict = {}
names_dict = {}

def loadCorpora():
    files =  glob.glob("../corpora/*.txt")
    for fileDir in files:
        print "Leyendo archivo "+fileDir
        loadFile(fileDir)
        

def loadFile(fileDir):
    corpora = fileDir.
    print "Terminado de cargar archivo " + fileDir + " con " , corpora.nsheets , " hojas"
    extractHashtags(corpora)

def changeCharacters(i):
    i = i.replace("\\xe1", "a")
    i = i.replace("\\xe0", "e")
    i = i.replace("\\xed", "i")
    i = i.replace("\\xf3", "o")
    i = i.replace("\\xfa", "u")
    i = i.replace("\\xc1", "A")
    i = i.replace("\\xe8", "E")
    i = i.replace("\\xda", "U")
    i = i.replace("\\xe9", "U")
    i = i.replace("\\xf1", "n")
    i = i.replace("\\xd1", "N")
    i = i.replace("\\xe3", "a")
    i = i.replace("\\xe7", "c")
    i = i.replace("\\xf9", "u")
    i = i.replace("\\xd3", "O")
    i = i.replace("\\xfc", "u")
    i = i.replace("\\xcd", "I")
    i = i.replace("\\xf2", "o")
    i = i.replace("\\xc9", "E")
    i = i.replace("\\xc3", "A")
    i = i.replace("\\xea", "e")
    i = i.replace("\\xe2", "a")
    i = i.replace("\\xec", "i")
    i = i.replace("\\xe4", "a")
    i = i.replace("\\xeb", "e")
    i = i.replace("\\xf4", "o")
    i = i.replace("\\xf5", "o")
    i = i.replace("\\xc0", "E")
    i = i.replace("\\xc7", "C")
    i = i.replace("\\xf6", "o")
    i = i.replace("\\xef", "i")
    i = i.replace("\\xc8", "E")
    i = i.replace("\\xdc", "U")
    i = i.replace("\\xd8", "o")
    i = i.replace("\\xd5", "o")
    i = i.replace("\\xd2", "O")
    i = i.replace("\\xc1", "A")
    return i

def extractHashtags(corpora):
    global hashtag_dict
    for sheet in corpora.sheets():
        for j in range(sheet.nrows):
            #Hashtag Extraction Begin ----------------------->
            if "[{" in sheet.cell_value(j,22):
                hashtags= (str(sheet.cell_value(j,22)[2:len(sheet.cell_value(j,22))-2]))
                hashtags = hashtags.replace("u'","'").replace("'","\"")
                for i in hashtags.split("}, {"):
                    i =  "{"+i+"}"
                    i = i.decode("latin1")
                    i = changeCharacters(i)
                    i = i.lower()
                    myjson = json.loads(i)
                    if(hashtag_dict.get(myjson['text'],"no_exist") != "no_exist"):
                        hashtag_dict[myjson['text']] = hashtag_dict[myjson['text']]+1
                    else:
                        hashtag_dict[myjson['text']] = 1
            #Hashtag Extraction End -------------------------------->
            #Users Extraction Begin ---------------------------->
            user = sheet.cell_value(j,18)
            user = changeCharacters(user)
            if(names_dict.get(user,"no_exist") != "no_exist"):
                names_dict[user] = names_dict[user] +1
            else:
                names_dict[user] = 1
            #Users Extraction End ----------------------------------->
    for v, k in sorted(((v, k) for k, v in hashtag_dict.items()), reverse=True)[0:30]:
       print k+" - "+str(v)
    for v, k in sorted(((v, k) for k, v in names_dict.items()), reverse=True)[0:30]:
       print k+" - "+str(v)

    return hashtag_dict
                 

    
if __name__ == '__main__':
   dict =  loadCorpora()

