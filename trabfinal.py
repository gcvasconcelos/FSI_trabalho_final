import config # python file with API keys
import tweepy
import json
import pandas as pd
import emoji
import re
import csv
import time

from textblob import TextBlob

# load positive words from dictionary
positives = []
positives_file = open('positivos.txt', 'r')
for word_file in positives_file:
  word_file = re.sub(r'\n', '', word_file.strip())
  positives.append(word_file)

# load positive emojis
positives_emojis = []
positives_emojis_file = open('emojis_positivos.txt', 'r')
for word_file in positives_emojis_file:
  word_file = re.sub(r'\n', '', word_file.strip())
  positives_emojis.append(word_file)

# load negative words from dictionary
negatives = []
negatives_file = open('negativos.txt', 'r')
for word_file in negatives_file:
  word_file = re.sub(r'\n', '', word_file.strip())
  negatives.append(word_file)

negatives_emojis = []
negatives_emojis_file = open('emojis_negativos.txt', 'r')
for word_file in negatives_emojis_file:
  word_file = re.sub(r'\n', '', word_file.strip())
  negatives_emojis.append(word_file)

def clean_tweet(tweet): 
  # remove ats
  tweet = re.sub(r'@(\w+)', '', tweet)
  # remove new lines
  tweet = re.sub(r'\n', ' ', tweet.strip())
  # remove links
  tweet = re.sub(r'https?:\/\/.*\/\w*', '', tweet.lower())
  # remove extra ponctuation
  tweet = re.sub(r'\.{2,}', '.', tweet)
  tweet = re.sub(r'\?{2,}', '?', tweet)
  tweet = re.sub(r'\!{2,}', '!', tweet)
  # remove ponctuation
  tweet = re.sub(r'\*', ' ', tweet)
  tweet = re.sub(r'\.', ' ', tweet)
  tweet = re.sub(r'\,', ' ', tweet)
  tweet = re.sub(r'\?', ' ', tweet)
  tweet = re.sub(r'\!', ' ', tweet)
  tweet = re.sub(r'\#', ' ', tweet)
  tweet = re.sub(r'\$', ' ', tweet)
  tweet = re.sub(r'\%', ' ', tweet)
  tweet = re.sub(r'\(', ' ', tweet)
  tweet = re.sub(r'\)', ' ', tweet)
  tweet = re.sub(r'\:', ' ', tweet)
  tweet = re.sub(r'\\', ' ', tweet)
  tweet = re.sub(r'\/', ' ', tweet)
  tweet = re.sub(r'\|', ' ', tweet)
  tweet = re.sub(r'\[', ' ', tweet)
  tweet = re.sub(r'\]', ' ', tweet)
  tweet = re.sub(r'\{', ' ', tweet)
  tweet = re.sub(r'\}', ' ', tweet)
  tweet = re.sub(r'\-', ' ', tweet)
  tweet = re.sub(r'\_', ' ', tweet)

  return tweet

def processing_tweet(tweet):
  tweet = re.sub(r'\bvc|voce\b', 'você', tweet)
  tweet = re.sub(r'\bpq\b', 'por que', tweet)
  tweet = re.sub(r'\bhj\b', 'hoje', tweet)
  tweet = re.sub(r'\bmt\b', 'muito', tweet)
  tweet = re.sub(r'\bq\b', 'que', tweet)
  tweet = re.sub(r'\bn\b', 'não', tweet)
  tweet = re.sub(r'\bt[ô|o]\b', 'estou', tweet)
  return tweet

def analyse_tweet(tweet_text):
  sentiment = 0
  text = tweet_text.split(" ")
  for word in text:
    for w_file in positives:
      if word == w_file:
        if sentiment <= 0:
          sentiment += 1
    for w_file in negatives:
      if word == w_file:
        if sentiment >= 0:
          sentiment -= 1
    for w_file in positives_emojis:
      if word == w_file:
        if sentiment <= 0:
          sentiment += 1
    for w_file in negatives_emojis:
      if word == w_file:
        if sentiment >= 0:
          sentiment -= 1
  
  return sentiment

def get_tweets(keyword):
  # pass twitter credentials to tweepy
  auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
  auth.set_access_token(config.access_key, config.access_secret)
  api = tweepy.API(auth)

  cursor = tweepy.Cursor(api.search, q=keyword, count=200, include_rts=False, since='2018-10-01', tweet_mode='extended', lang='pt')

  tweets = []
  for page in cursor.pages(1):
    for status in page:
      status = status._json
      tweet = status['full_text']
      
      # ignore retweets
      if (str(tweet[0:2]) == 'rt') or (str(tweet[0:2]) == 'RT'):
        continue
      tweet = clean_tweet(tweet)
      tweet_text = processing_tweet(tweet)
        
      sentiment = analyse_tweet(tweet_text)
      tweets.append({'tweet_id': status['id'], 'text': tweet_text, 'polarity': sentiment})
  
  return tweets

def eval_tweets(csv_name):
  sum_polarity = 0
  with open(csv_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      if row[0] != 'polarity':
        sum_polarity += int(row[0],10)

  return sum_polarity

def construct_dataset(csv_name, keywords):
  tweets = get_tweets(keywords)
  tweets_df = pd.DataFrame(tweets)
  tweets_df.drop_duplicates(subset='text', keep='first')
  tweets_df.to_csv(csv_name, encoding='utf-8', index=False)

  polarity_total = eval_tweets(csv_name)
  if polarity_total <= -15:
    classification = 'Péssimo'
  if -15 < polarity_total <= -5:
    classification = 'Meio ruim'
  if -5 < polarity_total <= 5:
    classification = 'Neutro'
  if 5 < polarity_total < 15:
    classification = 'Meio bom'
  if polarity_total >= 15:
    classification = 'Ótimo'

  print(polarity_total)
  print(classification)

keywords = ({
  'unb': 'unb,Universidade de Brasília,UnB, UNB',
  'engenharias': 'engenharia,curso de engenharia,FT',
  'cic': 'cic,comp,Ciência da Computação',
  'saude': 'medicina,enfermagem,veterinária',
  'humanas': 'filosofia,sociologia,ciência política'
  })

construct_dataset('unb_tweets_processed.csv', keywords['unb'])
