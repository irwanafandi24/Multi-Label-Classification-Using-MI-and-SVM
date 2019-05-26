# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:58:56 2019

@author: Asus
"""
import re #regular expression
from nltk.tokenize import word_tokenize #tokenisasi
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary #stopword

factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

#factory = StopWordRemoverFactory().get_stop_words()
#print(factory)
#more_stopword = ['afandi', 'mohamad', 'irwan', 'ganteng','unyu']
#data = factory + more_stopword
#dictionary = ArrayDictionary(data)
#str = StopWordRemover(dictionary)
##stopwords = factory.get_stop_words()
##stopword = factory.create_stop_word_remover(data)
#
kata = 'bagaimanapun jika kamu bersalah akan masuk penjara jika tidak ya tidak jika terbukti maka jika kamu mau'
print kata
print "===========Hasil Stopword========"
stopW = stopword.remove(kata)
print stopW
#a = str.remove(kata)
#print (data)
#print a




#from pylab import *
# 
#hLoss = [0.07321,0.07421,0.07471,0.07531,0.07621,0.07651,0.07681,0.07721,0.07781,0.07811,0.07921,0.08221,0.08421,0.08621,0.08921,0.09221,0.09721]
#feature = [30,40,50,60,70,80,90,100,110,120,130,150,160,170,180,190,200]
#plot(feature,hLoss)
# 
#xlabel('Feature Used')
#ylabel('Hamming Loss')
#title('Evaluasi Classification')
#grid(True)
#show()\
#
#arr=[]
#arr.append("Maka kerjakanlah apa yang dia minta")
#arr.append("berjuanglah sekuat tenaga selagi bisa")
#arr.append("nikmat mana yang selama ini kau dustakan")
#
#c = 0
#x = "maka kerjakan apa yang diminta"
#token = word_tokenize(x)
#
##new_bigrams = []
##while c < len(token) - 1:
##    new_bigrams.append((token[c], token[c+1]))
##    c+=1
#
#print token

