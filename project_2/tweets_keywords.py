# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:52:02 2021
@original author: Yalin Yener
@author: Juehao Lin, modified based on project: https://towardsdatascience.com/step-by-step-twitter-sentiment-analysis-in-python-d6f650ade58d
"""

from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer


consumerKey = '4es8FHoW3bgZulmNpT7PJb0F9'
consumerSecret = 'hJwu7Qsk5WTOpQKthfcw2HFQ7sz4ObUjmXokKzLL5zmhl3Gr5F'
accessToken = '1441943955159990280-JGh1mvaXSONFr8NbLz6AO2PoqwwpOK'
accessTokenSecret = '2TbtgnstIbx0XlU9S6AdDK1Qn3HQ2xS7DqTcImemxmf7X'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

def percentage(part,whole):
    return 100 * float(part)/float(whole)
keyword = input('Please enter keyword or hashtag to search: ' )
noOfTweet = int(input ('Please enter how many tweets to analyze: '))
tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(noOfTweet)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []
for tweet in tweets:
    #print(tweet.text)
    tweet_list.append(tweet.text)
    analysis = TextBlob(tweet.text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity
    if neg > pos:
         negative_list.append(tweet.text)
         negative += 1
    elif pos > neg:
         positive_list.append(tweet.text)
         positive += 1
    elif pos == neg:
         neutral_list.append(tweet.text)
         neutral += 1
     
positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')


tweet_list = pd.DataFrame(tweet_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
print('total number: ',len(tweet_list))
print('positive number: ',len(positive_list))
print('negative number: ', len(negative_list))
print('neutral number: ',len(neutral_list))

labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes,colors=colors, startangle=90)
plt.style.use('default')
plt.legend(labels)
plt.title('Sentiment Analysis Result for keyword= '+keyword+' with number of '+str(noOfTweet)+' tweets')
plt.axis('equal')
plt.show()