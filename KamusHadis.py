# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 00:04:19 2019

@author: Irwan
"""
from nltk.util import ngrams

def getKamusHadis(hadisContent,items):
    freq_word_a, freq_word_ba, freq_word_l, freq_word_bl, freq_word_i, freq_word_bi= {},{},{},{},{},{}
    sumWord, katake = 0,0
    for kalimat in hadisContent:                                                #access a hadis in an array
        for word in kalimat:                                                    #access every word in a hadis
            if items[katake].k1 == 1 :                                          #in anjuran class, label 1
                if word in freq_word_a:                                         #if word has been counted, so just add the sum of word
                    freq_word_a[word] +=1
                else:                                                           #if word not already in array (not counted yet)
                    freq_word_a[word] = 1                                       #add the  array with that word, and set the sum of word with 1
            else:                                                               #not in anjuran class
                if word in freq_word_ba:
                    freq_word_ba[word] +=1
                else:
                    freq_word_ba[word] = 1
        
            if items[katake].k2 == 1 :                                          #larangan class
                if word in freq_word_l:
                    freq_word_l[word] +=1
                else:
                    freq_word_l[word] = 1
            else:
                if word in freq_word_bl:
                    freq_word_bl[word] +=1
                else:
                    freq_word_bl[word] = 1
    
            if items[katake].k3 == 1 :                                          #informasi class
                if word in freq_word_i:
                    freq_word_i[word] +=1
                else:
                    freq_word_i[word] = 1
            else:
                if word in freq_word_bi:
                    freq_word_bi[word] +=1
                else:
                    freq_word_bi[word] = 1
            sumWord+=1
        katake+=1
    return freq_word_a, freq_word_ba, freq_word_l, freq_word_bl, freq_word_i, freq_word_bi, sumWord

def getBigramKamusHadis(hadisContent,items):
    freq_word_a, freq_word_ba, freq_word_l, freq_word_bl, freq_word_i, freq_word_bi= {},{},{},{},{},{}
    sumWord, katake = 0,0
    
    for kalimat in hadisContent:
        temp = []
        temp.append(list(ngrams(kalimat,2)))                                    #split word in to 2 word, and store it in  temp's array
        for x in temp:
            for word in x:
                if items[katake].k1 == 1 :                                      #anjuranclass
                    if word in freq_word_a:
                        freq_word_a[word] +=1
                    else:
                        freq_word_a[word] = 1
                else:
                    if word in freq_word_ba:
                        freq_word_ba[word] +=1
                    else:
                        freq_word_ba[word] = 1
            
                if items[katake].k2 == 1 :                                      #larangan class
                    if word in freq_word_l:
                        freq_word_l[word] +=1
                    else:
                        freq_word_l[word] = 1
                else:
                    if word in freq_word_bl:
                        freq_word_bl[word] +=1
                    else:
                        freq_word_bl[word] = 1
        
                if items[katake].k3 == 1 :                                      #informasi class
                    if word in freq_word_i:
                        freq_word_i[word] +=1
                    else:
                        freq_word_i[word] = 1
                else:
                    if word in freq_word_bi:
                        freq_word_bi[word] +=1
                    else:
                        freq_word_bi[word] = 1
                sumWord+=1
        katake+=1
    return freq_word_a, freq_word_ba, freq_word_l, freq_word_bl, freq_word_i, freq_word_bi, sumWord

def getValueHadis(hadis,k):                                                     #all hadis item, k =1,2,3 (1 anjuran, 2 larangan, 3 informasi)
    kelas = []
    for value in hadis:
        if k==1:
            kelas.append(int(value.k1))                                         #get all label in anjuran
        if k==2:
            kelas.append(int(value.k2))                                         #get all label in larang
        if k==3:
            kelas.append(int(value.k3))                                         #get all label in informasi
    return kelas

def getAllWordHadis(hadisContent):
    freq_word = {}
    for kalimat in hadisContent:
        for word in kalimat:
            if word in freq_word:
                freq_word[word] +=1
            else:
                freq_word[word] = 1
    return freq_word

def getBigramAllWordHadis(hadisContent):
    freq_word = {}
    for kalimat in hadisContent:
        temp = []
        temp.append(list(ngrams(kalimat,2))) 
        for x in temp:
            for word in x:
                if word in freq_word:
                    freq_word[word] +=1
                else:
                    freq_word[word] = 1
    return freq_word

def wordInHadis(hadisCategory):                                                 #sum word in a class, dictionary {word,value}
    sumWordKata,b=0,0
    for i in hadisCategory:
        b= hadisCategory.get(i)                                                 #get sum of word
        sumWordKata = sumWordKata+b
    return sumWordKata