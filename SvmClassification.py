# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:02:18 2019

@author: Irwan
"""
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

def classification(X_train, y_train, X_test): 
    clf = svm.SVC(kernel='linear', gamma = 'scale', C=1)
#    clf = svm.SVC(kernel='rbf', gamma = 'scale')
#    clf = svm.SVC(kernel='poly', gamma = 'scale')
#    clf = svm.SVC(kernel='sigmoid', gamma = 'scale')
  
#    clf = KNeighborsClassifier(n_neighbors=5)   
#    clf= MultinomialNB()
#    clf= MLPClassifier(solver='adam', alpha=0.0001, hidden_layer_sizes=(75, 10), random_state=1, max_iter=250)  
    
    clf.fit(X_train, y_train)
    clf_predictions = clf.predict(X_test)
    return clf_predictions