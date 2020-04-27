#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 17:35:31 2019

@author: soumyaram
"""

file=open("/Users/soumyaram/Downloads/2018districts.txt", "r")
count=0
listy=[]
num=["0","1","2", "3","4", "5", "6", "7", "8", "9"]
for line in file:
    line.replace("\t","")

    if "Retiring" not in line and "Running" not in line and "Ran" not in line:
        for i in range(len(line)):
            if line[i] in num:
                if line[i+1] in num:
                    numy=line[i]+line[i+1]
                else:
                    numy=line[i]
                break
        counter=0
        if line.split(" ")[0]=="New":
            ans=line.split(" ")[0]+ " "+line.split(" ")[1]
        else:
            ans=line.split(" ")[0]
        listy.append([ans,numy])


outF = open("2018ACTUALdistrict.txt", "w")
for line in listy[:-1]:
  # write line to output file
  outF.write(line[0]+" " + line[1])
  outF.write("\n")
outF.close()
