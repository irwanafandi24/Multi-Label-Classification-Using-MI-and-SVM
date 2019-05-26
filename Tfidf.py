# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 08:39:26 2019

@author: Irwan
"""
import numpy as np
import math
from nltk.util import ngrams

def getTf(feature,hadisContent):
    cSentence,tfTable =0, np.array([[0 for x in range (len(hadisContent)+1)] for y in range(len(feature))],dtype=object) #kolom x baris
    for hadisFeature in feature:                                                #access each feature are used from feature selection
        cDocument = 0                                                           #number of word 
        tfTable[cSentence][cDocument]= hadisFeature                             #every [number][0] fill with feature
        for document in hadisContent:
            countWord =0
            for sentence in document:                                           #access each word in sentence hadis
                if hadisFeature == sentence:
                    countWord+=1                                                #count the sum of feature active in that document
            cDocument+=1
            tfTable[cSentence][cDocument] =countWord                            #every [feature-x][doc-x] = count that feature  ==> [word, val doc 1, val2, ..,vallas feature]
        cSentence+=1
    return tfTable

def getIdf(feature,hadisContent):
    idfTable = np.array([[0 for x in range (0,2)] for y in range(len(feature))],dtype=object)
    countRow = 0            
    for wordFeature in feature:
        idfTable[countRow][0] = wordFeature
        countdf = float(0)
        for document in hadisContent:
            countSenInWord = 0
            for sentence in document:
                if wordFeature == sentence:                                     #if the feature found in hadith word
                    countSenInWord+=1                                           #flag to give the sign that the hadith have that feature
                    break                                                       #out from loop, just need one word
            if countSenInWord > 0:                                              #1 mean document contain that feature, 0 mean not yet
                countdf+=1                                                      #the number of hadith that contain that feature
        idfTable[countRow][1] =math.log10((len(hadisContent)/countdf))          #get idf value
        countRow+=1
    return idfTable

def getTfidf(tfTable, idfTable,feature,hadisContent):
    tfidfTable = np.array([[0 for x in range (len(hadisContent))] for y in range(len(feature))],dtype=float)
    countRow=0
    for i in tfTable:                                                           #access tf data
        for j in idfTable:                                                      #access idf data
            if i[0] == j[0]:                                                    #conditional if tf data equal to idf data
                for col in range(len(hadisContent)):                            #this loop use for fill the tf-idf feature in all document
                    tfidfTable[countRow][col] = float(i[col+1]*j[1])            #column is feature, left is document
                break;
        countRow+=1
    return tfidfTable.T                                                         #transpose, column is document row is feature

def getTfBigram(feature,hadisContent):                                          #TF for bigram model
    cSentence,tfTable =0, np.array([[0 for x in range (len(hadisContent)+1)] for y in range(len(feature))],dtype=object) #kolom x baris
    for hadisFeature in feature:
        cDocument = 0
        tfTable[cSentence][cDocument]= hadisFeature
        for document in hadisContent:
            temp = []
            temp.append(list(ngrams(document,2))) 
            countWord =0
            for x in temp:
                for sentence in x:
                    if hadisFeature == sentence:
                        countWord+=1
            cDocument+=1
            tfTable[cSentence][cDocument] =countWord
        cSentence+=1
    return tfTable

def getIdfBigram(feature,hadisContent):                                         #IDF for bigram model
    idfTable = np.array([[0 for x in range (0,2)] for y in range(len(feature))],dtype=object)
    countRow = 0            
    for wordFeature in feature:
        idfTable[countRow][0] = wordFeature
        countdf = float(0)
        for document in hadisContent:
            temp = []
            temp.append(list(ngrams(document,2))) 
            countSenInWord = 0
            for x in temp:
                for sentence in x:
#                    print wordFeature, '   ', sentence
                    if wordFeature == sentence:
                        countSenInWord+=1
                        break
            if countSenInWord > 0:
                countdf+=1
        idfTable[countRow][1] =math.log10((len(hadisContent)/countdf))
        countRow+=1
    return idfTable

def getTfidfBigram(tfTable, idfTable,feature,hadisContent):                     #TFIDF for bigram model
    tfidfTable = np.array([[0 for x in range (len(hadisContent))] for y in range(len(feature))],dtype=float)
    countRow=0
    for i in tfTable:
        for j in idfTable:
            if i[0] == j[0]:
                for col in range(len(hadisContent)):
                    tfidfTable[countRow][col] = float(i[col+1]*j[1])
                break;
        countRow+=1
    return tfidfTable.T

#this just for input tfidf

def getTfInput(feature,hadisContent):                                           #TF input to predict
    cSentence,tfTable =0, np.array([[0 for x in range (0,2)] for y in range(len(feature))],dtype=object) #kolom x baris
    for hadisFeature in feature:
        cDocument = 0
        tfTable[cSentence][cDocument]= hadisFeature
#        for document in hadisContent:
        countWord =0
        for sentence in hadisContent:
            if hadisFeature == sentence:
                countWord+=1
        cDocument+=1
        tfTable[cSentence][cDocument] =countWord
        cSentence+=1
    return tfTable

def getTfidfInput(tfTable, idfTable,feature,hadisContent):                      #TFIDF iinput  predict
    tfidfTable = np.array([[0 for x in range (0,1)] for y in range(len(feature))],dtype=float)
    countRow=0
    for i in tfTable:
        for j in idfTable:
            if i[0] == j[0]:
                for col in range(0,1):
                    tfidfTable[countRow][col] = float(i[col+1]*j[1])
                break;
        countRow+=1
    return tfidfTable.T