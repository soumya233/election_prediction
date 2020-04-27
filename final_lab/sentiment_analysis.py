#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:01:30 2019

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

training_points=[]
training_labels=[]
test_class_points=[]
test_class_labels=[]
test_reg_points=[]
test_reg_labels=[]
candidates_to_features={}

years = ["2014", "2016", "2018"]
dates_to_years={"2014":[dt.date(2014,10,28),dt.date(2014,11,3)],"2016":[dt.date(2016,11,1),dt.date(2016,11,7)], "2018":[dt.date(2018,10,31),dt.date(2018,11,6)]}
for year in years:
    date_list=dates_to_years[year]
    # candidates = pd.read_csv("{}.csv".format(year), delimiter = "|")
    candidates = []
    with open('{}.txt'.format(year), 'r') as f:
        for lines in f:
            lines = lines.replace(u'\n', '')
            candidates.append(lines.split('|'))
    pairs = int(len(candidates)/2)
    for i in range(pairs):
        candidate_names = [candidates[2*i][3], candidates[2*i+1][3], float(candidates[2*i][4])-float(candidates[2*i+1][4])]
## FOR I IN CANDIDATE NAMES#########
    # candidate_names=["Opponent1", "Opponent2"]
        test_reg_points.append(np.array(candidate_names[2]))
        winner=0
        a=np.random.uniform(1)
        if a > 0.5:
            candidate_names=[candidate_names[1],candidate_names[0]]
            winner=1
        test_class_points.append(np.array(winner))
        new_candidate_names=[]
        for i in candidate_names:
            ans=i.split(" ")
            new_candidate_names.append(ans[0]+ans[-1])
        feature_vector=[]
        test_for_year=[]
        for i in range(len(new_candidate_names)):
            list_of_tweets = query_tweets(new_candidate_names[i], begindate=date_list[0],enddate=date_list[1])
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
                neutral_score+=score['neutral']
            length=len(list_of_tweets)
            pos_score=pos_score/length
            neg_score=neg_score/length
            neutral_score=neutral_score/length
            feature_vector+=[pos_score,neg_score,neutral_score,length]
            candidates_to_features[candidate_names[i]]=feature_vectors

        
        if year == "2014":
            training_points.append(feature_vector)
            training_labels.append(winner)
        elif year == "2016":
            test_class_points.append(feature_vector)
            test_class_labels.append(winner)
        else:
            test_reg_points.append(feature_vector)
            test_reg_labels.append(winner)


regressor = LinearRegression()
regressor.fit(training_points, training_labels)
regressor.score(test_class_points, test_class_label)

clf = SVC()
clf.fit(training_points, training_labels) 
clf.score(test_class_points, test_class_labels)
all_data = {"training points": [training_points,training_labels], "test_class_points":[test_class_points,test_class_labels],
            "test_reg_points": [test_reg_points,tes_reg_labels], "candidates_to_features":candidates_to_features, "clf":clf, "regressor":regressor}
pickle.dump(all_data,open("save_all_data.p", "wb" ))
