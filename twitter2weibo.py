#!/usr/bin/env python
# Repost tweets of specific user to Sina Weibo
# Author: LIU Yang <gloolar@gmail.com>
# 2017.11

import tweepy
import pickle
from datetime import datetime, timedelta
from weibo import Client
import urllib
import sys
import time

# Reposted Twitter user IDs
# HistoryInPix, ClassicPixs
twitter_ids = ['1557315432', '1407123690']

# ----------------------------------------------------------------------------
# Load last creation dates

pkfile = 'pickledata.pk'

try:
    with open(pkfile, 'rb') as fi:
      records = pickle.load(fi)
except EnvironmentError:
    records = {}
    for id in twitter_ids:
        records[id] = {'last_date': datetime.now() - timedelta(hours=2.5)}
    with open(pkfile, 'wb') as fi:
        pickle.dump(records, fi)

# ----------------------------------------------------------------------------
# Collect new tweets

t_auth = tweepy.OAuthHandler(t_consumer_key, t_consumer_secret)
t_auth.set_access_token(t_access_token, t_access_token_secret)
t_api = tweepy.API(t_auth)

tweets = []

for user_id in twitter_ids:
    for status in tweepy.Cursor(t_api.user_timeline, id=user_id).items():
        if status.created_at < records[user_id]['last_date']:
            break

        author_id = status.author.id_str
        # media = status.extended_entities.get('media')
        media = status.entities.get('media')

        if (author_id == user_id) and (media is not None) and (not status.text.startswith('RT')):
            tweets.append({
                'author_id': author_id,
                'author_screen_name': status.author.screen_name,
                'text': status.text,
                'media_urls': [m['media_url'] for m in media],
                'creation_date': status.created_at})

if len(tweets) == 0:
    sys.exit()
else:
    print("%d new tweets got" % len(tweets))
    # print(tweets)

# ----------------------------------------------------------------------------
# Post to Weibo, and update last date records

w_client = Client(w_api_key, w_api_secret, w_redirect_uri, w_token)

for tweet in reversed(tweets):
    w_status = tweet['text'] + ' (RT @' + tweet['author_screen_name'] + ')'
    urllib.urlretrieve(tweet['media_urls'][0], 'temp.jpg')
    w_client.post('statuses/share', status=w_status, pic=open('temp.jpg', 'rb'))
    # Udpate last tweet date for author_id
    records[tweet['author_id']]['last_date'] = tweet['creation_date']
    # Wait some time
    time.sleep(60*3) # 3 minutes

# ----------------------------------------------------------------------------
# Save records to disk
with open(pkfile, 'wb') as fi:
    pickle.dump(records, fi)

