#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:46:14 2019

@author: soumyaram
"""
import os
import pickle
import numpy as np
path="indices/"
listy=os.listdir(path)

from sklearn.svm import SVC
training_points=[]
training_label=[]


for i in listy:
    if "save" in i:
        with open(path+i,"rb") as f:
            try:
            
                train_small=pickle.load(open(path+i,"rb"))["training_points"][0]
                test_small=pickle.load(open(path+i,"rb"))["training_points"][1]
    
                training_points+=train_small
                training_label+=test_small
                
            except:
                try:
                    train_small=pickle.load(open(path+i,"rb"))["training points"][0]
                    test_small=pickle.load(open(path+i,"rb"))["training points"][1]
    
                    training_points+=train_small
                    training_label+=test_small
                
                
                
                
                except:

                    train_small=pickle.load(open(path+i,"rb"))[0]
        
                    test_small=pickle.load(open(path+i,"rb"))[1]
                    training_points+=train_small
                    training_label+=test_small

        f.close()
 ##randomly permute results
for i in range(len(training_points)):
    a=np.random.uniform(0,1)
    if a > 0.5:

        training_points[i]=training_points[i][4:8]+training_points[i][0:4]
        training_label[i]=0
###############################
        

        

clf = SVC()
clf.fit(training_points, training_label) 
print("2014")
print(clf.score(training_points, training_label))


path="indices2018/"
listy=os.listdir(path)

val_points=[]
val_label=[]


def preprocess(listy):
    new_listy=[]
    for i in listy:
        if type(i)==list:
            new_listy.append(i)
        #else:
            #print(i)
    return new_listy


for i in listy:
    if "save" in i:
        with open(path+i,"rb") as f:
            try:

                train_small=preprocess(pickle.load(open(path+i,"rb"))["test_reg_points"][0])
                test_small=pickle.load(open(path+i,"rb"))["test_reg_points"][1]

                val_points+=train_small
                val_label+=test_small

                
            except:

                #print(pickle.load(open(path+i,"rb")))
                train_small=preprocess(pickle.load(open(path+i,"rb"))[0])
    
                test_small=pickle.load(open(path+i,"rb"))[1]
                val_points+=train_small
                val_label+=test_small

        f.close()
 ##randomly permute results
for i in range(len(val_label)):
    a=np.random.uniform(0,1)
    if a > 0.5:
        #print(i,len(training_points))

 
        val_points[i]=val_points[i][4:8]+val_points[i][0:4]
        val_label[i]=0



#print(len(training_points))
#print(len(test_points))



path="indices2016/"
listy=os.listdir(path)

test_points=[]
test_label=[]



for i in listy:
    if "save" in i:
        with open(path+i,"rb") as f:
            try:

                train_small=preprocess(pickle.load(open(path+i,"rb")["test_class_points"][0]))
                test_small=pickle.load(open(path+i,"rb"))["test_class_points"][1]

                test_points+=train_small
                test_label+=test_small

                
            except:

                #print(pickle.load(open(path+i,"rb")))
                train_small=preprocess(pickle.load(open(path+i,"rb"))[0])
    
                test_small=pickle.load(open(path+i,"rb"))[1]
                test_points+=train_small
                test_label+=test_small

        f.close()
 ##randomly permute results
for i in range(len(test_label)):
    a=np.random.uniform(0,1)
    if a > 0.5:
    
        test_points[i]=test_points[i][4:8]+test_points[i][0:4]
        test_label[i]=0

max_value=0
max_clf=0


for i in range(600):
    clf = SVC(probability=True)
    clf.fit(val_points, val_label) 
    val_score=clf.score(test_points, test_label)
    if val_score> max_value:
        max_value=val_score
        max_clf=clf

print(max_value)
print(max_clf.score(training_points,training_label))
    
pickle.dump(clf,open("clfchosen.p","wb"))
