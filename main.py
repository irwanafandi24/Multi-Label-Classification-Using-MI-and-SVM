# -*- coding: utf-8 -*-1
"""
Created on Sat Feb  2 19:19:27 2019

@author: Irwan Afandi
"""
import time
import operator #shorting
import numpy as np
import Preprocessing as pr
import KamusHadis as kms
import MutualInformation as mi
import SvmClassification as cl
from xlrd import open_workbook #open file
from sklearn.model_selection import KFold


startTime = time.time()

wb = open_workbook('data.xlsx')
hadisContent, items = pr.openFile(wb)                                           #Save only word of hadith and all data hadith into array
#get word hadis
content = []
for i in hadisContent:                                                          #store every hadis in 1 array
    content.append(i)

print("Preprosessing")
hadisContent = pr.preprocessingProcess(hadisContent)                            #preprocessing (clean, casefold, stopword, stem, token)
valueAnjuran     =kms.getValueHadis(items, 1)                                   #get all Anjuran Label
valueLarangan    =kms.getValueHadis(items, 2)                                   #get all Larangan Label
valueInformasi   =kms.getValueHadis(items, 3)                                   #get all Information Label
arr1, arr2, arr3 =np.array(valueAnjuran,dtype=np.int64), np.array(valueLarangan,dtype=np.int64), np.array(valueInformasi,dtype=np.int64)
arr              =[arr1,arr2,arr3]                                              #Marge 3 array to one array

#a0,a1 = (arr1 == 0).sum(),(arr1 == 1).sum()                                    #get hadis in class anjuran (1) and doesn't on anjuran(0)
#b0,b1 = (arr2 == 0).sum(),(arr2 == 1).sum()
#c0,c1 = (arr3 == 0).sum(),(arr3 == 1).sum()                                           

print("finish preprosessing")

kf,count, hloss = KFold(n_splits=10, random_state=None, shuffle=False),0,[]
pred0, pred1, pred2 = [],[],[]                                                  #to save all predict data 1-1064
for train_index, test_index in kf.split(hadisContent):
    dataTrain, dataTest, dataItems = [],[],[]
    count +=1;
    for i in range (len(train_index)):
        dataTrain.append(hadisContent[train_index[i]])                          #get train data every fold
        dataItems.append(items[train_index[i]])                                 #get train hadis and class every fold
    for i in range (len(test_index)):
        dataTest.append(hadisContent[test_index[i]])                            #get test data every fold

    freq_word_a, freq_word_ba, freq_word_l, freq_word_bl, freq_word_i, freq_word_bi, sumWord= kms.getKamusHadis(dataTrain,dataItems)         #unigram
#    freq_word_a, freq_word_ba, freq_word_l, freq_word_bl, freq_word_i, freq_word_bi, sumWord= kms.getBigramKamusHadis(dataTrain,dataItems)  #bigram

    freq_word = kms.getAllWordHadis(dataTrain)                                                          # unigram all word in hadis and sum every word
#    freq_word = kms.getBigramAllWordHadis(dataTrain)                                                   # bigram
    
    sumWordA, sumWordBA = kms.wordInHadis(freq_word_a), kms.wordInHadis(freq_word_ba)                   #sum All ward in one hadis category
    sumWordL, sumWordBL = kms.wordInHadis(freq_word_l), kms.wordInHadis(freq_word_bl)
    sumWordI, sumWordBI = kms.wordInHadis(freq_word_i), kms.wordInHadis(freq_word_bi)
  
    wordA  = sorted(freq_word_a.items(), key=operator.itemgetter(0))                                    #sorted word of hadith A-Z (0 is word, 1 sum of word)
    wordBA = sorted(freq_word_ba.items(), key=operator.itemgetter(0))
    wordL  = sorted(freq_word_l.items(), key=operator.itemgetter(0))
    wordBL = sorted(freq_word_bl.items(), key=operator.itemgetter(0))
    wordI  = sorted(freq_word_i.items(), key=operator.itemgetter(0))
    wordBI = sorted(freq_word_bi.items(), key=operator.itemgetter(0))
  
    larangan  = mi.confusionMatrixValue(wordL, wordBL, sumWordL,sumWordBL)                              #get Confusional Matrix of hadith data
    anjuran   = mi.confusionMatrixValue(wordA, wordBA, sumWordA, sumWordBA)
    informasi = mi.confusionMatrixValue(wordI, wordBI,sumWordI, sumWordBI)

    miLarangan  = mi.miValue(larangan,(sumWord))                                                        #get MI value every word in hadith class
    miAnjuran   = mi.miValue(anjuran,(sumWord))
    miInformasi = mi.miValue(informasi,(sumWord))

    allMiValue  = []
    allMiValue.append(miLarangan[0])
    margeLarangan = mi.margeMiValue(miLarangan,allMiValue)
    margeAnjuran  = mi.margeMiValue(miAnjuran,margeLarangan)
    margeMi       = mi.margeMiValue(miInformasi,margeAnjuran)                                           #get word with Mi value (same, take higest) for all hadith
    
    def getKey(item):
        return item.value
    
#    allHadisSortedByValue = sorted(freq_word.items(), key=operator.itemgetter(1),reverse=True)
    #featureX = []                                                                                      #get feature without MI
    #for i in allHadisSortedByValue:     
    #    featureX.append(i[0])
           
    featureX = sorted(margeMi, key=getKey, reverse=True)                                                #sorted feature from higest mi value (9-1)
#    for i in range (0,100):
#        print "Kata1: ",featureX[i].hadis,"===",featureX[i].value

    #===================================Save===================================
#    print("Get Feature Word with MI")
#    title = "FeatureMI"+str(count)+".xls"
#    mi.toExcelMI(title,"sheet1",featureX)                                                              #save all unigram feature
#    mi.toExcelAllFeature(title,"sheet1",allHadisSortedByValue)                                         #save all unigram feature without feature selection
    
#    title = "FeatureMIBigram"+str(count)+".xls"
#    mi.toExcelMIBigram(title,"sheet1",featureX)                                                        #save all bigram feature  
    #==========================================================================
    
    repeatCount = 30
    while(repeatCount<=30):
        import Tfidf as tfidf
    #    cntFitur = round(len(featureX)*(repeatCount/100))
        feature  = []
        for i in range(0,repeatCount):
            feature.append(featureX[i].hadis)  
#            feature.append(allHadisSortedByValue[0])                               #uncoment this if use no MI, and comment the code above

        
        #==================== Unigram
        tfTrain = tfidf.getTf(feature,dataTrain)                                    #get TF Value
        idfTrain = tfidf.getIdf(feature,dataTrain)                                  #get IDF Value
        tfidfTrain = tfidf.getTfidf(tfTrain, idfTrain,feature,dataTrain)            #get TF-IDF
        
        tfTest = tfidf.getTf(feature,dataTest)                                      
        tfidfTest = tfidf.getTfidf(tfTest, idfTrain,feature,dataTest)               #TFIDF test = tf test x idf train
        #==================== Bigram
#        tfTrain = tfidf.getTfBigram(feature,hadisContent)                          #get TF Bigram Value
#        idfTrain = tfidf.getIdfBigram(feature,hadisContent)                        #get IDF Bigram Value
#        tfidfTrain = tfidf.getTfidfBigram(tfTrain, idfTrain,feature,dataTrain)     #get TF-IDF  Bigram
#        
#        tfTest = tfidf.getTfBigram(feature,dataTest)                                      
#        tfidfTest = tfidf.getTfidfBigram(tfTest, idfTrain,feature,dataTest)
        #=========================

        xTrain, xTest = tfidfTrain, tfidfTest
        p0,p1,p2 = [],[],[]                                                     #to store predict label
        r0,r1,r2 = [],[],[]                                                     #to store real label
        for c, y in enumerate(arr):                                             #this will access class one by one ==>binary relevance
            yTrain, yTest = y[train_index], y[test_index]
#            print len(yTrain)
            predictValue = cl.classification(xTrain, yTrain, xTest)
            if c == 0:                                                          #anjuran
                p0.append(predictValue)                                         #predict label from testing data
                r0.append(yTest)                                                #real label testing
            elif c == 1:                                                        #larangan
                p1.append(predictValue)
                r1.append(yTest)
            elif c==2:                                                          #informasi
                p2.append(predictValue)
                r2.append(yTest)  
#============================================================================== #get the sum valu 0 or 1 in class every fold                
#        atm00,atm01,atm10,atm11,atm20,atm21=0,0,0,0,0,0                        #to know the sum data in class and doesn't in class
#        for i in range(len(p0[0]))                                             #please uncomment line 35-37 to make this work 
#            if r0[0][i] == 0:
#                atm00+=1
#            elif r0[0][i] == 1:
#                atm01+=1
#                
#            if r1[0][i] == 0:
#                atm10+=1
#            elif r1[0][i] == 1:
#                atm11+=1
#                
#            if r2[0][i] == 0:
#                atm20+=1
#            elif r2[0][i] == 1:
#                atm21+=1
#     
#        print a0-atm00,' | ' ,a1-atm01
#        print b0-atm10,' | ' ,b1-atm11
#        print c0-atm20,' | ' ,c1-atm21        
#==============================================================================
        #get all prediksi 
        for i in range(len(p0[0])): 
            pred0.append(p0[0][i])                                              #record anjuran prediction from 1-1064
            pred1.append(p1[0][i])                                              #record larangan prediction from 1-1064
            pred2.append(p2[0][i])                                              #record informasi prediction from 1-1064
       
        missclass = 0
        for i in range (len(p0[0])):                                            #length test only 106 or 107
             if p0[0][i] != r0[0][i]:                                           #cek predict equals real label or nat
                 missclass+=1                                                   #if not missclassification ++
             if p1[0][i] != r1[0][i]:
                 missclass+=1
             if p2[0][i] != r2[0][i]:
                 missclass+=1
        hammingloss = 1/float(len(p0[0]))*1/float(len(arr))*missclass           #get hamming loss in k =1 repeat till 10
        print "K-fold ke-",count," Nilai Hamming loss: ", hammingloss
        hloss.append(hammingloss)                                               #save hamming loss every fold
        repeatCount+=10
print "Rata-rata halosss: ",np.mean(hloss)                                      #average hamming loss from 10 fold
pr.saveHasil("HasilPrediksiSistem.xls","hasilprediksi",content, pred0, pred1, pred2)    #save the predict value