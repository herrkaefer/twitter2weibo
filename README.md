`twitter2weibo`: Repost interested tweets to Sina Weibo.

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

# Reposted Twitter user IDs
twitter_ids = ['xxx', 'xxx']

```

Then conduct a schedule to run `twitter2weibo.py`, on a server.
