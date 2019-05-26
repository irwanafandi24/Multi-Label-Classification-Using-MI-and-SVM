# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 00:30:26 2019

@author: Irwan
"""

import re #regular expression
from nltk.tokenize import word_tokenize #tokenisasi
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory #stopword
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory #stemming
import xlwt

factori = StemmerFactory()
stemmer = factori.create_stemmer()
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

class hadisClass(object):
    def __init__(self,hadis,k1,k2,k3):
        self.hadis = hadis
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3     
        
def openFile(wb):        
    hadisContent, items= [],[]                                                  #take only the word, take all items hadith
    for sheet in wb.sheets():
        num_row, num_col = sheet.nrows, 4                                       #size for all the document 1064, just take 4 data till class 
        for row in range(num_row):                                              #access the active row (has been filled)
            values = []
            for col in range(num_col):
                if col == 0:
                    x = (sheet.cell(row,col).value)
                value = (sheet.cell(row,col).value)
                values.append(value)                                            #values is array filled with hadis anc class
            hadisContent.append(x)
            item = hadisClass(*values)                                          #create object hadis
            items.append(item)                                                  #items array of hadis object
    return hadisContent, items

def preprocessingProcess(hadisContent):
    for i in range (len(hadisContent)):
        print(i)
        cleanning = re.sub('[^a-zA-z\s]','', hadisContent[i])                   #cleanning
        casefold = cleanning.lower();                                           #case folding
#        stopW = stopword.remove(casefold)                                      #stopword removal
#        stemming = stemmer.stem(stopW)                                         #stemming    ==> bikin lama frooh
#        word_tokens = word_tokenize(stopW)                                     #tokenisasi 
#        word_tokens = word_tokenize(stemming)
        word_tokens = word_tokenize(casefold) 
        
        hadisContent[i]=word_tokens
    return hadisContent

def preprocessingInput(hadisContent):                                           #just for input data from keyboard
    cleanning = re.sub('[^a-zA-z\s]','', hadisContent)                          #cleanning
    casefold = cleanning.lower();                                               #case folding
#        stopW = stopword.remove(casefold)                                      #stopword removal
#        stemming = stemmer.stem(casefold)                                      #stemming    ==> bikin lama frooh
#        word_tokens = word_tokenize(stemming)                                  #tokenisasi 
    word_tokens = word_tokenize(casefold)
    return word_tokens

def saveHasil(filename, sheet, content, p1, p2, p3):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    n=0

    for i in range(len(content)):
        sh.write(n,0,content[i])
        sh.write(n,1,str(p1[i]))
        sh.write(n,2,str(p2[i]))
        sh.write(n,3,str(p3[i]))
        n+=1
        
    book.save('Output/'+filename) 