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
  # clean = ' '.join(re.sub(r"(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())

  # detect emojis and convert to string
  # tweet = emoji.demojize(tweet) 
  return tweet

def remove_features(tweet):
  # detect emojis and convert to string
  # tweet = emoji.demojize(tweet) 
  emoji.get_emoji_regexp().sub(u'', tweet)
  return emoji.get_emoji_regexp().sub(u'', tweet)

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
      tweet = clean_tweet(status['full_text'])
      # ignore retweets
      if tweet[0:2] == 'rt':
        continue
      tweets.append({'tweet_id': status['id'], 'text': tweet})
  
  return tweets

def analyse_tweet(tweets_df):
  total = 0
  sentiments = []
  for index, tweet in tweets_df.iterrows():
    tweet = remove_features(tweet['text'])
  
    translator = Translator()
    text_en = translator.translate(tweet, src='pt', dest='en')
    # text_pt = TextBlob(tweet)
    # text_en = TextBlob(str(text_pt.translate(from_lang='pt', to='en')))
    
    text_en = TextBlob(text_en.text)
    polarity = text_en.sentiment.polarity

    if polarity > 0:
      sentiment = 1
    elif polarity < 0:
      sentiment = -1
    else:
      sentiment = 0
    sentiments.append(sentiment)
    total += 1
    print(total)
  
  tweets_df['polarity'] = sentiments
  return tweets_df

def construct_dataset(csv_name):
  tweets = get_tweets('unb')
  tweets_df = pd.DataFrame(tweets)
  tweets_df = analyse_tweet(tweets_df)
  tweets_df.to_csv(csv_name, encoding='utf-8', index=False)

# construct_dataset('unb_tweets.csv')
