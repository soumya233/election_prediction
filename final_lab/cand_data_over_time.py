#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 12:44:26 2019

@author: soumyaram
"""

import pandas as pd
import os
import pickle
import numpy as np
ans=pd.read_csv("Elections2020CloseRaces - Sheet1 (1).csv",header=None)
cand_to_fv={}
path=""
file_list=os.listdir(path)
fv={}

date_to_list={}

date_list=["2019-09-07","2019-08-07","2019-10-07","2019-11-07","2019-12-07"]
for k in date_list:
    for i in file_list:
        if k in i:
            fv.update(pickle.load(open(path+i,"rb")))
    
    clf=pickle.load(open("clfchosen.p","rb"))
    district_dems={}
    district_repub={}
    for i in ans.iterrows():
        if i[1].iloc[0] in district_dems and i[1].iloc[2]=="D":
            district_dems[i[1].iloc[0]].append(i[1].iloc[1])
        elif i[1].iloc[2]=="D":
            district_dems[i[1].iloc[0]]=[i[1].iloc[1]]
        if i[1].iloc[0] in district_repub and i[1].iloc[2]=="R":
            district_repub[i[1].iloc[0]].append(i[1].iloc[1])
        elif i[1].iloc[2]=="R":
            district_repub[i[1].iloc[0]]=[i[1].iloc[1]]
    
    district_dem_pred={}
    district_repub_pred={}
    for i in district_dems:
        names=district_dems[i]
        winner=names[0]
        for j in range(len(names)-1):
            index=clf.predict(np.reshape(fv[winner]+fv[names[j+1]],(1,-1)))[0]
            winner=[winner,names[j+1]][index]
        district_dem_pred[i]=winner
    for i in district_repub:
        names=district_repub[i]
        winner=names[0]
        for j in range(len(names)-1):
            index=clf.predict(np.reshape(fv[winner]+fv[names[j+1]],(1,-1)))[0]
            winner=[winner,names[j+1]][index]
        district_repub_pred[i]=winner
    final_dict={"person":[],"party":[],"prob_of_dem_win":[],"state":[],"district":[]}
    prob_of_dem_win=[]
    for i in district_dem_pred:

        final_dict["person"].append(district_dem_pred[i])
        final_dict["person"].append(district_repub_pred[i])
        final_dict["party"].append("D")
        final_dict["party"].append("R")
        final_dict["state"].append(" ".join(i.split(" ")[:-1]))
        final_dict["state"].append(" ".join(i.split(" ")[:-1]))
        final_dict["district"].append(i.split(" ")[-1])
        final_dict["district"].append(i.split(" ")[-1])
        inputy=np.reshape(fv[district_dem_pred[i]]+fv[district_repub_pred[i]],(1,-1))        
        prob_of_dem_win.append(clf.predict_proba(inputy)[0][0])
        prob_of_dem_win.append(clf.predict_proba(inputy)[0][0])

    date_to_list[k]=prob_of_dem_win

    
del final_dict["prob_of_dem_win"]
final_dict.update(date_to_list)
df=pd.DataFrame.from_dict(final_dict)
    
df.to_csv(k+".csv")
