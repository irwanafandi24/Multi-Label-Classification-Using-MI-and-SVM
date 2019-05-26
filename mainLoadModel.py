# -*- coding: utf-8 -*-1
"""
Created on Sat Feb  2 19:19:27 2019

@author: Irwan Afandi
"""
import time
import numpy as np
import Preprocessing as pr
import KamusHadis as kms
import MutualInformation as mi
import SvmClassification as cl
from pylab import *
from xlrd import open_workbook #open file
from nltk.util import ngrams
from sklearn.model_selection import KFold

startTime = time.time()

wb = open_workbook('data.xlsx')
hadisContent, items = pr.openFile(wb)                       #Save only word of hadith and all data hadith into array

print("Preprosessing")
hadisContent = pr.preprocessingProcess(hadisContent)        #preprocessing (clean, casefold, stopword, stem, token)
valueAnjuran     =kms.getValueHadis(items, 1)                #get all Anjuran Label
valueLarangan    =kms.getValueHadis(items, 2)                #get all Larangan Label
valueInformasi   =kms.getValueHadis(items, 3)                #get all Information Label
arr1, arr2, arr3 =np.array(valueAnjuran,dtype=np.int64), np.array(valueLarangan,dtype=np.int64), np.array(valueInformasi,dtype=np.int64)
arr              =[arr1,arr2,arr3]                           #Marge 3 array to one array
print("finish preprosessing")

repeatCount, acc, ftr =30, 1, 0
arrFitur, arrHamming = [], []
while(repeatCount<=30):
    import Tfidf as tfidf
    fold, hloss = 0, []
    kf,count = KFold(n_splits=10, random_state=None, shuffle=False),0
    for train_index, test_index in kf.split(hadisContent):
        dataTrain, dataTest, dataItems = [],[],[]
        fold +=1;
        for i in range (len(train_index)):
            dataTrain.append(hadisContent[train_index[i]])
            dataItems.append(items[train_index[i]])
        for i in range (len(test_index)):
            dataTest.append(hadisContent[test_index[i]])   
       
        #==================LOAD FEATURE=======================
        #unigram
        titleMI = "Data_feature/FeatureMI"+str(fold)+".xls"
        wb = open_workbook(titleMI)
        featureLoad = mi.loadMI(wb)
        
        #bigram
#        titleMI = "Data_Feature_Bigram/FeatureMIBigram"+str(fold)+".xls"
#        wb = open_workbook(titleMI)
#        featureLoad = mi.loadMIBigram(wb)
        
        feature  = []
        for i in range(0,repeatCount):
            feature.append(featureLoad[i])
        #==================== TFIDF Unigram
        tfTrain = tfidf.getTf(feature,dataTrain)                     #get TF Value
        idfTrain = tfidf.getIdf(feature,dataTrain)                   #get IDF Value
        tfidfTrain = tfidf.getTfidf(tfTrain, idfTrain,feature,dataTrain)  #get TF-IDF
        
        tfTest = tfidf.getTf(feature,dataTest)  
        tfidfTest = tfidf.getTfidf(tfTest, idfTrain,feature,dataTest)

        #==================== TFIDF Bigram
#        tfTrain = tfidf.getTfBigram(feature,hadisContent)                     #get TF Bigram Value
#        idfTrain = tfidf.getIdfBigram(feature,hadisContent)                   #get IDF Bigram Value
#        tfidfTrain = tfidf.getTfidfBigram(tfTrain, idfTrain,feature,dataTrain)  #get TF-IDF  Bigram
#        
#        tfTest = tfidf.getTfBigram(feature,dataTest)                                      
#        tfidfTest = tfidf.getTfidfBigram(tfTest, idfTrain,feature,dataTest)
        #===========================
        
        xTrain, xTest = tfidfTrain, tfidfTest
        p0,p1,p2 = [],[],[]
        r0,r1,r2 = [],[],[]
        for c, y in enumerate(arr):
            yTrain, yTest = y[train_index], y[test_index]
            predictValue = cl.classification(xTrain, yTrain, xTest)
            if c == 0:
                p0.append(predictValue)
                r0.append(yTest)
            elif c == 1:
                p1.append(predictValue)
                r1.append(yTest)
            elif c==2:
                p2.append(predictValue)
                r2.append(yTest)
                
        #==================== hamming loss        
        missclass = 0
        trueData = 0
        for i in range (len(p0[0])):
             if p0[0][i] != r0[0][i]:
                 missclass+=1
             if p1[0][i] != r1[0][i]:
                 missclass+=1
             if p2[0][i] != r2[0][i]:
                 missclass+=1
#             if p0[0][i] == r0[0][i] and p1[0][i] == r1[0][i] and p2[0][i] == r2[0][i]:
#                 trueData +=1

        
#        akurasi = float(trueData)/float(107)*100
        print akurasi
        hammingloss = 1/float(len(p0[0]))*1/float(len(arr))*missclass
        hloss.append(hammingloss) 
        
        
        
    avgHloss = np.mean(hloss)
    arrFitur.append(repeatCount)
    arrHamming.append(avgHloss)
    
    
    print 'Feature: ',repeatCount,'  | Rata-rata halosss: ',avgHloss
    if(acc>avgHloss):
        acc, ftr = avgHloss, repeatCount
    repeatCount+=10
print('==================================================================')
print 'Time              : ',time.time()-startTime,'second'
print 'Best Hamming loss : ', acc
print 'Feature used      : ', ftr

plot(arrFitur,arrHamming)
 
xlabel('Feature Used')
ylabel('Hamming Loss')
title('Evaluasi Classification')
grid(True)
show()

#============================================================ input hadith data
inputhadis = raw_input("Please type the hadith: ")
inputhadis = pr.preprocessingInput(inputhadis)

titleMI = "Data_feature/FeatureMI7.xls"
wb = open_workbook(titleMI)
featureLoad = mi.loadMI(wb)

feature  = []
for i in range(0,ftr):
    feature.append(featureLoad[i])
    
tfTrain = tfidf.getTf(feature,hadisContent)                     #get TF Value
idfTrain = tfidf.getIdf(feature,hadisContent)                   #get IDF Value
tfidfTrain = tfidf.getTfidf(tfTrain, idfTrain,feature,dataTrain)  #get TF-IDF
tfTest = tfidf.getTfInput(feature,inputhadis)     
                               
tfidfTest = tfidf.getTfidfInput(tfTest, idfTrain,feature,inputhadis)

xTrain, xTest = tfidfTrain, tfidfTest
hadisIndex = []
for i in range (0,1064):
    hadisIndex.append(i)
predict1, predict2, predict3 = [],[],[]
for c, y in enumerate(arr):
    yTrain = y[train_index]
    predictValue = cl.classification(xTrain, yTrain, xTest)
    if c == 0:
        predict1.append(predictValue)
    elif c == 1:
        predict2.append(predictValue)
    elif c==2:
        predict3.append(predictValue)
print "Kelas Prediksi"
print predict1[0],predict2[0],predict3[0]
print "==========================================="
if predict1[0] == 1:
    keterangan1 = "Anjuran"
else: 
    keterangan1 = "Bukan Anjuran"
if predict2[0] == 1:
    keterangan2 = "Larangan"
else: 
    keterangan2 = "Bukan Larangan"
if predict3[0] == 1:
    keterangan3 = "Informasi"
else: 
    keterangan3 = "Bukan Informasi"

print "Hadis tersebut tergolong hadis: ",keterangan1," | ",keterangan2," | ", keterangan3