# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 08:14:26 2019

@author: Irwan
"""

import math
import xlwt

class confusionalTable(object):
    def __init__(self,hadis,bb,bs,sb,ss):
        self.hadis = hadis
        self.bb = bb
        self.bs = bs
        self.sb = sb
        self.ss = ss
        
class miClass(object):
    def __init__(self,hadis,value):
        self.hadis = hadis
        self.value = value

def confusionMatrixValue(wordTrue, wordFalse,sumWordTrue, sumWordFalse):        #format wordTrue [(word,value)]
    confusionMatrix = []
    itemsBB, itemsBS,itemsSB, itemsSS=0,0,0,0
    for items in wordTrue:
        values = []
        itemsWord, itemsBB = items[0],items[1]                                  #get the word and BB value
        values.append(itemsWord)                                                #value[0] = word
        for searchItem in wordFalse:
            if items[0] == searchItem[0]:                                       #condition to check, is there word x (wordTrue) in array wordFalse
                itemsBS = searchItem[1]
                break
            else:
                itemsBS=0                                                       #get value BS from condition
        itemsSB = sumWordTrue-itemsBB                                           #get value SB
        itemsSS = sumWordFalse-itemsBS                                          #get value SS
        values.append(float(itemsBB))                                           #value[1] = BB 
        values.append(float(itemsBS))                                           #value[2] = BS
        values.append(float(itemsSB))                                           #value[3] = SB
        values.append(float(itemsSS))                                           #value[4] = SS
        confTable = confusionalTable(*values)                                   #truth is the object of confusionalTable
        confusionMatrix.append(confTable)                                       #array of object confusionalTable
    return confusionMatrix

def miValue(tabelHadis,N):
    miTable=[]
    N = float(N)
    for kata in tabelHadis:                                                                         #access every object of confusional matrix
        valMi = []
        BB =(kata.bb/N)*math.log(((kata.bb*N)/((kata.bb+kata.bs)*(kata.bb+kata.sb))),2)             #get miValue of BB
        if kata.bs == 0:                                                                            #if BS_matrix = 0, miValue of BS = 0
            BS =0
        else:    
            BS =(kata.bs/N)*math.log(((kata.bs*N)/((kata.bs+kata.bb)*(kata.bs+kata.ss))),2)         #get miValue of BS
        SB =(kata.sb/N)*math.log(((kata.sb*N)/((kata.sb+kata.bb)*(kata.sb+kata.ss))),2)             #get miValue of SB
        SS =(kata.ss/N)*math.log(((kata.ss*N)/((kata.ss+kata.bs)*(kata.ss+kata.sb))),2)             #get miValue of SS
        miWord = (BB+BS+SB+SS)                                                                      #get miValue of that WORD
        valMi.append(kata.hadis)
        valMi.append(miWord)
        mi=miClass(*valMi)
        miTable.append(mi)                                                                          #array of object miClass                                                          
    return miTable

def margeMiValue(miTable, margeTable):
    for x in miTable:                                                           #access data from miValue data that will be marge
        count,a=0,0
        for i in margeTable:                                                    #access data from miValue marge table, read all data
            if(x.hadis == i.hadis):                                             #if word in miValue_data already in miValue marge
                if(x.value>=i.value):                                           #if in miValue_data greater than miValue marge
                    margeTable[count]=x                                         #repleace that position with value from mi_valu_data
                a+=1                                                            #to give flaq a = 1 mean word is already in miValue_marge
                break
            count+=1
        if(a==0):                                                               #a = 0 mean, there isn't that ward in miValue_marge
            margeTable.append(x)                                                #just insert miValu_date[x] to miValue_marge
    return margeTable                                                           #array of object miClass ==> (word,value)

def toExcelAllFeature(filename, sheet, listMi):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    n=0

    for i in listMi:
        sh.write(n,0,i[0])
        sh.write(n,1,i[1])
        n+=1
        
    book.save('Data_feature_noMI/'+filename) 

def toExcelMI(filename, sheet, listMi):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    n=0

    for i in range(len(listMi)):
        sh.write(n,0,listMi[i].hadis)
        sh.write(n,1,listMi[i].value)
        n+=1
        
    book.save('Data_feature_noMI/'+filename) 

def toExcelMIBigram(filename, sheet, listMi):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    n=0

    for i in range(len(listMi)):
        count = 0
        for x in listMi[i].hadis:
            if count == 0:
                sh.write(n,0,x)
            elif count == 1:
                sh.write(n,1,x)
            count+=1
        sh.write(n,2,listMi[i].value)
        n+=1
        
    book.save('Data_Feature_Bigram/'+filename)   
    
def loadMI(wb):
    fitur = []
    for sheet in wb.sheets():
        num_row, num_col = sheet.nrows, 1
        for row in range(num_row):
            for col in range(num_col):
                fitur.append(sheet.cell(row,col).value)
    return fitur

def loadMIBigram(wb):
    fitur = []
    for sheet in wb.sheets():
        num_row, num_col = sheet.nrows, 2
        for row in range(num_row):
            kata1,kata2="",""
            for col in range(num_col):
                if col == 0:
                    kata1 = sheet.cell(row,col).value
                elif col == 1:
                    kata2 = sheet.cell(row,col).value
            bigramKata = (kata1,kata2)
            fitur.append(bigramKata)
    return fitur        