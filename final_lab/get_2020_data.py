#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:27:59 2019

@author: soumyaram
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.svm import SVC
from twitterscraper import query_tweets
import datetime as dt
import re
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

candidates_to_features={}
range_index=1
years = ["2014", "2016", "2018"]
#dates_to_years={"2014":[dt.date(2014,10,28),dt.date(2014,11,3)],"2016":[dt.date(2016,11,1),dt.date(2016,11,7)], "2018":[dt.date(2018,10,31),dt.date(2018,11,6)]}

date_list=[dt.date(2019,8,7),dt.date(2019,8,8)]
    
#ranges=[(0,pairs//4),(pairs//4, 2*pairs//4),(2*pairs//4,3*pairs//4),(3*pairs//4,pairs)]
candidate_names=['Lucy McBath', 'Karen Handel', 'Abby Finkenauer', 'Ashley Hinson', 'Rita Hart', 'Bobby Schilling', 'Cindy Axne', 'Brad Huss', 'Bill Schafer', 'David Young', 'Carolyn Bourdeaux', 'Lynne Homrich', 'Renee Unterman', 'Richard McCormick', 'Lauren Underwood', 'Jim Oberweis', 'Sue Rezin', 'Jared Goldman', 'Eric Brakey', 'Elissa Slotkin', 'Mike Detmer', 'Paul Junge', 'Nikki Snyder', 'Kristina Lyke ', 'Collin Peterson', 'Michelle Fischbach', 'Jeff Van Drew', 'Brian Fitzherbert', 'Bob Patterson ', 'David Richter', 'Andy Kim', 'Kate Gibbs', 'John Novak', 'Antonio Delgado', 'Tony German', 'Ola Hawatmeh', 'Mike Roth ', 'Ben McAdam', 'Mia Love', 'Kathleen Anderson', 'Elaine Luria', 'Ben Loyola', 'Betsy Londrigan', 'Stefanie Smith', 'Rodney Davis', 'Beth Van Duyne', 'Jan McDowell', 'Kim Olson', 'Scott Perry', 'Eugene DePasquale', 'Xochitl Torres Small', 'Yvette Herrell', 'Max Rose', 'Nicole Malliotakis', 'Anthony Brindisi', 'Claudia Tenney', 'Kendra Horn', 'Stephanie Bice', 'Terry Neese', 'Joe Cunningham', 'Nancy Mace', 'Kathy Landing']


k=2
    
for i in range(k*len(candidate_names)//3,(k+1)*len(candidate_names)//3):
    list_of_tweets = query_tweets(candidate_names[i], begindate=date_list[0],enddate=date_list[1])
    analyser = SentimentIntensityAnalyzer()
    pos_score=0
    neg_score=0
    neutral_score=0
    for tweet in list_of_tweets:
        stringy=tweet.text
        stringy = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', stringy)
        stringy = re.sub(r'http\S+', '', stringy)
        stringy = re.sub(r'#([^\s]+)', r'\1', stringy)
        score = analyser.polarity_scores(stringy)
        pos_score+=score['pos']
        neg_score+=score['neg']
        neutral_score+=score['neu']
    length=len(list_of_tweets)
    if length != 0:
        pos_score=pos_score/length
        neg_score=neg_score/length
        neutral_score=neutral_score/length
    else:
        (pos_score,neg_score,neutral_score)=(0,0,0)

    candidates_to_features[candidate_names[i]]=[pos_score,neg_score,neutral_score,length]

pickle.dump(candidates_to_features,open(str(date_list[0])+"-"+str(i)+".p", "wb" ))
