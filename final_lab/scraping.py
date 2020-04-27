import os
import pandas as pd

# dem_candidates = [["Hillary Clinton", "Clinton", "2015-04-12"]]
# rep_candidates = [["Donald Trump", "Trump","2015-03-18"]]

# for candidate in rep_candidates:
#     # os.system('twitterscraper "{}" -bd {} -ed 2016-11-09 -o {}_tweets.json'.format(candidate[1], candidate[2], candidate[1]))
#     os.system('twitterscraper "{}" -bd 2016-11-02 -ed 2016-11-09 -o {}_tweets.json -l 10000'.format(candidate[1], candidate[1]))
years = ['2014', '2016', '2018']
for year in years: 
    yearlist = []
    with open('{}_swing.txt'.format(year)) as f:
        for line in f:
            line = line.replace(u'\xa0', ' ')
            line = line.replace(u'\n', '')
            line = line.replace(u'\t', '')
            state, district = line.rsplit(' ', 1)
            if district == 'at-large':
                district = '0'
            yearlist.append(state + district )

    winners = []
    data = pd.read_csv('1976-2018-house.csv', delimiter = ',', encoding='latin1')
    candidates = data[data['year'].isin([year])]
    candidates['candidatevotes'] = candidates['candidatevotes'].str.replace(',','')
    candidates['candidatevotes'] = pd.to_numeric(candidates['candidatevotes'])
    candidates['totalvotes'] = pd.to_numeric(candidates['totalvotes'])
    candidates['statedistrict'] = candidates['state'] + candidates['district'].apply(str)
    # candidates['totalvotes'] = candidates['totalvotes'].str.replace(',','')
    # candidates['totalvotes'] = candidates['totalvotes'].apply(int)
    candidates['proportion'] = candidates['candidatevotes']/candidates['totalvotes']

    a = candidates.sort_values(['year', 'district', 'state', 'proportion'], ascending=[True, True, True, False])
    swing = candidates['statedistrict'].isin(yearlist)
    trainyear = a[swing].groupby(['year', 'district', 'state']).head(2)[['district', 'state', 'candidate','proportion', 'party']]
    
    trainyear.to_csv('{}.txt'.format(year), sep='|', header=False)
# print(train2014.groupby(['district','state']).size().reset_index().rename(columns={0:'count'}).sort_values(['state', 'district']))