import tweepy
from settings import consumer_key, consumer_secret

def twitter_authentication_url ():
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  try:
    auth_url = auth.get_authorization_url(signin_with_twitter=True)
  except tweepy.TweepError:
    #tweet failed
    return None

  return (auth_url, auth.request_token.key, auth.request_token.secret)

def twitter_authenticate (verifier, request_token, request_secret):
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
  auth.set_request_token(request_token, request_secret)

  try:
    auth.get_access_token(verifier)
  except tweepy.TweepError:
    return None

  return (auth.access_token.key, auth.access_token.secret)

def twitter_post (access_token, access_secret, text):
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  api = tweepy.API(auth)
  api.update_status(text)

def twitter_home_timeline (access_token, access_secret, count):
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  api = tweepy.API(auth)
  statuses = api.home_timeline(count=count)

  status_list = []
  for status in statuses:
    status_list.append({'text': status.text,
                        'time': status.created_at,
                       'user': {'name': status.user.name}})

  return status_list;

