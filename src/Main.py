'''
Created on 25/09/2013

@author: juan
'''

import glob
import xlrd
import json
import re



def loadCorpora():
    files =  glob.glob("../corpora/*.xls")
    for fileDir in files:
        print "Leyendo archivo "+fileDir
        loadFile(fileDir)
        

def loadFile(fileDir):
    corpora = xlrd.open_workbook(fileDir, encoding_override='utf-8')
    print "Terminado de cargar archivo " + fileDir + " con " , corpora.nsheets , " hojas"
    extractHashtags(corpora)

    
def extractHashtags(corpora):
    for sheet in corpora.sheets():
        nrows = sheet.nrows
        ncols = sheet.ncols
        for i in range(sheet.nrows):
            if "[{" in sheet.cell_value(i,22):
                print "Item " ,sheet.cell_value(i,22)[2:len(sheet.cell_value(i,22))-2]
                hashtags= (str(sheet.cell_value(i,22)[2:len(sheet.cell_value(i,22))-2]))
                hashtags = hashtags.replace("u'","'").replace("'","\"")
                for i in hashtags.split("}, {"):
                    i =  "{"+i+"}"
                    value = unicode(i)
                    value = value.encode('ascii','xmlcharrefreplace')
                    print value
                    json.loads(value)
                    #json.loads(fixed)
                 
    
if __name__ == '__main__':
    loadCorpora()