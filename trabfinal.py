import config # python file with API keys
import tweepy
import json
import pandas as pd
from textblob import TextBlob
from googletrans import Translator
import emoji
import re

def clean_tweet(tweet): 
  # remove ats
  tweet = re.sub(r'@(\w+)', '', tweet)
  # remove new lines
  tweet = re.sub(r'\n', ' ', tweet.strip())
  # remove links
  tweet = re.sub(r'https?:\/\/.*\/\w*', '', tweet.lower())
  # detect and remove emojis 
  tweet = emoji.get_emoji_regexp().sub(u'', tweet)
  # remove extra ponctuation
  tweet = re.sub(r'\.{2,}', '.', tweet)
  tweet = re.sub(r'\?{2,}', '?', tweet)
  tweet = re.sub(r'!{2,}', '!', tweet)
  return tweet

def processing_tweet(tweet):
  tweet = re.sub(r'\bvc|voce\b', 'você', tweet)
  tweet = re.sub(r'\bpq\b', 'por que', tweet)
  tweet = re.sub(r'\bhj\b', 'hoje', tweet)
  tweet = re.sub(r'\bmt\b', 'muito', tweet)
  tweet = re.sub(r'\bq\b', 'que', tweet)
  tweet = re.sub(r'\bt[ô|o]\b', 'estou', tweet)
  return tweet

def analyse_tweet(tweet_text):  
  translator = Translator()
  text_en = translator.translate(tweet_text, src='pt', dest='en')

  # text_pt = TextBlob(tweet_text)
  # blob = TextBlob(str(text_pt.translate(from_lang='pt', to='en')))
  
  # blob = TextBlob(text_en.text)
  polarity = blob.sentiment.polarity

  if polarity > 0:
    sentiment = 1
  elif polarity < 0:
    sentiment = -1
  else:
    sentiment = 0 
  return sentiment

def get_tweets(keyword):
  # pass twitter credentials to tweepy
  auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
  auth.set_access_token(config.access_key, config.access_secret)
  api = tweepy.API(auth)

  cursor = tweepy.Cursor(api.search, q=keyword, count=200, include_rts=False, since='2018-10-01', tweet_mode='extended', lang='pt')

  tweets = []
  for page in cursor.pages(5):
    for status in page:
      status = status._json
      tweet = status['full_text']
      # ignore retweets
      if tweet[0:2] == 'rt':
        continue
      tweet = clean_tweet(tweet)
      tweet_text = processing_tweet(tweet)
      
      sentiment = analyse_tweet(tweet_text)
      tweets.append({'tweet_id': status['id'], 'text': tweet_text, 'polarity': sentiment})
  
  return tweets

def construct_dataset(csv_name):
  tweets = get_tweets('unb')
  tweets_df = pd.DataFrame(tweets)
  tweets_df.drop_duplicates(subset='text', keep='first')
  tweets_df.to_csv(csv_name, encoding='utf-8', index=False)

construct_dataset('unb_tweets_processed.csv')
