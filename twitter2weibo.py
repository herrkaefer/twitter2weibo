#!/usr/bin/env python
# encoding: utf-8
# Repost tweets of specific user to Sina Weibo
# Author: LIU Yang <gloolar@gmail.com>
# Created: 2017.11

import tweepy
import weibo
import pickle
from datetime import datetime, timedelta
import urllib.request
import os
import time
import pytz
from pid.decorator import pidfile
import appconfig as cfg


print("--------------------------------------")
print("Run at: " + str(datetime.now(pytz.utc)) + "\n")

# ----------------------------------------------------------------------------
# Load last creation dates

here = os.path.dirname(os.path.abspath(__file__))
pkfile = os.path.join(here, cfg.pkfile)
tweet_start_time = datetime.now(pytz.utc) - timedelta(hours=9)


# Load records of last update or create it if missing.
try:
    with open(pkfile, 'rb') as fi:
        records = pickle.load(fi)
    for id in cfg.twitter_ids:
        if records.get(id) is None:
            records[id] = {'last_date': tweet_start_time}
except EnvironmentError:
    records = {}
    for id in cfg.twitter_ids:
        records[id] = {'last_date': tweet_start_time}


# ----------------------------------------------------------------------------
def save_records():
    with open(pkfile, 'wb') as fi:
        pickle.dump(records, fi)


def fetch_recent_tweets(from_datetime):
    """Collect new tweets"""
    t_auth = tweepy.OAuthHandler(cfg.t_consumer_key, cfg.t_consumer_secret)
    t_auth.set_access_token(cfg.t_access_token, cfg.t_access_token_secret)
    t_api = tweepy.API(t_auth)

    tweets = []

    try:
        for user_id in cfg.twitter_ids:
            print("checking user with id: " + user_id)
            for status in tweepy.Cursor(
                    t_api.user_timeline, id=user_id).items():
                # offset-naive -> offset_aware
                tweet_created_at = \
                    status.created_at.replace(tzinfo=pytz.utc)
                if tweet_created_at <= records[user_id]['last_date'] \
                   or tweet_created_at < from_datetime:
                    break
                print("Tweet created at: " + str(status.created_at))
                author_id = status.author.id_str
                # media = status.extended_entities.get('media')
                media = status.entities.get('media')

                if (author_id == user_id
                   and media is not None
                   and (not status.text.startswith('RT'))):
                    tweets.append({
                        'author_id': author_id,
                        'author_screen_name': status.author.screen_name,
                        'text': status.text,
                        'media_urls': [m['media_url'] for m in media],
                        'creation_date': tweet_created_at
                    })
    except Exception as e:
        print(e)
        return []

    print("%d new tweets got." % len(tweets))
    return tweets


# ----------------------------------------------------------------------------
def post_to_weibo(tweets):
    """Post to Weibo, and update last date records"""
    w_client = weibo.Client(cfg.w_api_key, cfg.w_api_secret,
                            cfg.w_redirect_uri, cfg.w_token)
    try:
        for idx, tweet in enumerate(reversed(tweets)):
            print("\npost to weibo: ")
            # w_status = tweet['text']  # + ' (RT @' + tweet['author_screen_name'] + ')'
            w_status = tweet['text'] + ' ' + cfg.secure_domain + ' '
            print(w_status)
            urllib.request.urlretrieve(tweet['media_urls'][0], 'temp.jpg')
            w_client.post(
                'statuses/share', status=w_status, pic=open('temp.jpg', 'rb'))
            # Udpate last tweet date for author_id
            records[tweet['author_id']]['last_date'] = tweet['creation_date']
            if idx < len(tweets) - 1:
                print("wait a minute.")
                time.sleep(60*3)
    except Exception as e:
        print(e)
        raise
    finally:
        print("Update records to disk.")
        with open(pkfile, 'wb') as fi:
            pickle.dump(records, fi)
    print("done.")


@pidfile(piddir=here)
def main():
    tweets = fetch_recent_tweets(tweet_start_time)
    post_to_weibo(tweets)
    save_records()


if __name__ == '__main__':
    main()
