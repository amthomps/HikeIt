#Change the output
#Compare TF-IDF BOW cosine similarity of search term with all trip reports, summarize recent trip reports
import pandas as pd
import re
from gensim import corpora, models, similarities
from six.moves import cPickle as pickle
import matplotlib as mpl, matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
dfgrouped = pd.read_csv('dfgrouped2.csv')

import numpy as np
np.random.seed(2018)

with open('dictionary.pickle', 'rb') as file_handle:
    dictionary = pickle.load(file_handle)

with open('tfidf.pickle', 'rb') as file_handle:
    tfidf = pickle.load(file_handle)

with open('corpus_tfidf.pickle', 'rb') as file_handle:
    corpus_tfidf = pickle.load(file_handle)

def SimilarityModel(userinput  = 'Default', topicinput = 'TrailConditions'):
    #narrow search to ones that have the topicinput
    with open('fullwithsent.pickle', 'rb') as file_handle:
        fullwithsent = pickle.load(file_handle)

    topicdf = fullwithsent[fullwithsent['topic'] == 'TrailConditions']
    hikelist = list(set(list(topicdf['hikename'])))

    vec_bow = dictionary.doc2bow(userinput.lower().split())
    vec_tfidf = tfidf[vec_bow]
    index = similarities.MatrixSimilarity(corpus_tfidf) # transform corpus to LSI space and index it
    index.save('/tmp/tripreporter.index')
    index = similarities.MatrixSimilarity.load('/tmp/tripreporter.index')
    sims = index[vec_tfidf]
    hikerec = pd.DataFrame(sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)[:5])
    hikerec.columns = ['index', 'score']
    #pd.merge(hikerec, dfgrouped, on = 'index', how = 'left')
    hikedf = pd.merge(hikerec, dfgrouped, on = 'index', how = 'left')

    #filter hikedf for hikename being in hikelist
    hikedf = hikedf[hikedf['hikename'].isin(hikelist)]
    #round decimal places
    hikedf['score'] = hikedf['score'].round(decimals = 3)

    hikename = list(hikedf['hikename'])[:5]
    score = list(hikedf['score'])[:5]

    negtext = []
    negdate = []
    negurl = []
    postext = []
    posdate = []
    posurl = []
    imgname = []
    count = 0
    for hike in hikename:
        count = count + 1
        if hike in list(fullwithsent['hikename']):
            testdf = fullwithsent[fullwithsent['hikename'] == hike]
            SummaryTable = pd.DataFrame(testdf.groupby('topic')['tripreporturl'].count())
            SummaryTable['mean'] = testdf.groupby('topic')['Sentiment'].mean()
            SummaryTable['topic'] = SummaryTable.index
            topicnames = ['TrailConditions', 'Dogs', 'Camping', 'Bugs', 'Wildlife', 'RoadCondtions', 'WaterFeatures' 'Difficulty', 'Flora', 'Snow', 'Weather', 'Views']
            SummaryTable = SummaryTable[SummaryTable['topic'].isin(topicnames)]

            #if len(SummaryTable) > 0:
            #    mpl.use('agg')
            #    plt.figure(figsize=(2,2))
            #    ax = sns.barplot(y = 'topic', x = 'tripreporturl', data = SummaryTable, dodge = False, palette = mpl.cm.RdBu(SummaryTable['mean']/2+0.5), edgecolor=".2")
            #    ax.set(xlabel='Number of Reports', ylabel='Topic')
            #    name = str('new_plot' + str(count) + '.png')
            #    #savepath = str('flaskexample/static/' + name)
            #    #plt.savefig(savepath)
            #    imgname.append(name)
                #plt.show()

            testdf = testdf[testdf['topic'] == topicinput]
            testdf['paragraph'].replace('', np.nan, inplace=True)
            testdf.dropna(subset=['paragraph'], inplace=True)
            testdf['datetime'] = pd.to_datetime(testdf['date'])


            #negperson = testdf[testdf['Sentiment'] == min(testdf['Sentiment'])]
            #negperson['paragraph'] = negperson['paragraph'].str.replace(r'\xa0', ' ')
            #negtext.append(negperson['paragraph'].tolist()[0])
            #negdate.append(negperson['date'].tolist()[0])
            #negurl.append(negperson['tripreporturl'].tolist()[0])
            para = ''
            dat = ''
            tru = ''
            if len(testdf) > 0:
                recperson = testdf[testdf['datetime'] == max(testdf['datetime'])]
                recperson['paragraph'] = recperson['paragraph'].str.replace(r'\xa0', ' ')
                para = recperson['paragraph'].tolist()[0]
                dat = recperson['date'].tolist()[0]
                tru = recperson['tripreporturl'].tolist()[0]
            postext.append(para)
            posdate.append(dat)
            posurl.append(tru)

    return hikename, score, postext, posdate, posurl, imgname, topicinput, userinput
