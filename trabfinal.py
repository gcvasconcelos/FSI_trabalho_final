import config # python file with API keys
import tweepy
import json
import pandas as pd
import re

def clean_tweet(tweet): 
  # remove ats
  tweet = re.sub(r'@(\w+)', '', tweet)
  # remove new lines
  tweet = re.sub(r'\n', ' ', tweet.strip())
  # remove links
  tweet = re.sub(r'https?:\/\/.*\/\w*', '', tweet.lower())
  # clean = ' '.join(re.sub(r"(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())
  return tweet

def get_tweets(keyword):
  # pass twitter credentials to tweepy
  auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
  auth.set_access_token(config.access_key, config.access_secret)
  api = tweepy.API(auth)

  cursor = tweepy.Cursor(api.search, q=keyword, count=200, include_rts=False, since='2018-10-01', tweet_mode='extended', lang='pt')

  tweets = []
  for page in cursor.pages(20):
    for status in page:
      status = status._json
      tweet = clean_tweet(status['full_text'])
      # ignore retweets
      if tweet[0:2] == 'rt':
        continue
      tweets.append({'id': status['id'], 'tweet': tweet})
  
  return tweets

def construct_dataset(csv_name):
  tweets = get_tweets('unb')
  tweets_df = pd.DataFrame(tweets)
  tweets_df.to_csv(csv_name, encoding='utf-8', index=False)

construct_dataset('unb_tweets.csv')