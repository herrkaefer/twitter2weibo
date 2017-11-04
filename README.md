`twitter2weibo`: Post tweets of interested Twitter IDs to Sina Weibo.

# Demo

Weibo ID [@图中看史](https://weibo.com/u/6401135522) which reposts great pictures from several Twitter IDs.

# How to use

First, create Twitter and Weibo apps. Put private settings into a `appconfig.py` file along with `twitter2weibo.py`, which looks like:

```py
t_consumer_key = 'xxx'
t_consumer_secret = 'xxx'
t_access_token = 'xxx'
t_access_token_secret = 'xxx'

w_api_key = 'xxx'
w_api_secret = 'xxx'
w_redirect_uri = 'xxx'
w_token = 'xxx'

# Reposted Twitter IDs
twitter_ids = ['xxx', 'xxx']

```

On a server, install missing packages:

```sh
pip install weibo, tweepy
```

Then conduct a schedule to run `twitter2weibo.py` on the server.

# Notes

- Weibo has limitation of post rate, so keep your tweets timeline in a normal range.
- Only original tweets with media are collected. Only the first picture is posted due to Weibo API limitation.
