import tweepy
from settings import DEBUG

if DEBUG:
  consumer_key="NTuzgYZY3fCMMQcIDn73Xg"
  consumer_secret="9NAvbXWoZktTQYb9BHTQnMtleNq6UBJXlbsDUWJY"
else:
  consumer_key="FL6V9vrWlfVKzpFVB0iDmg"
  consumer_secret="Td8Mn4BzStppzPNDblylAibTXmDfRt0gjzN1cFAI"

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
    status_list.append(_parse_status(status))

  return status_list;

def _parse_status (status):
  return {'contributors': status.contributors,
          'truncated': status.truncated,
          'text': status.text,
          'in_reply_to_status_id': status.in_reply_to_status_id,
          'id': status.id,
          'author': _parse_user (status.author),
          'retweeted': status.retweeted,
          'coordinates': status.coordinates,
          'source': status.source,
          'in_reply_to_screen_name': status.in_reply_to_screen_name,
          'id_str': status.id_str,
          'retweet_count': status.retweet_count,
          'in_reply_to_user_id': status.in_reply_to_user_id,
          'favorited': status.favorited,
          #'retweeted_status': _parse_status (status.retweeted_status),
          'source_url': status.source_url,
          'user': _parse_user (status.user),
          'geo': status.geo,
          #'in_reply_to_user_str': status.in_reply_to_user_str,
          'created_at': _parse_datetime (status.created_at),
          #'in_reply_to_status_id_str': status.in_reply_to_status_id_str,
          'place': status.place}

def _parse_user (user):
  return {'follow_request_sent': user.follow_request_sent,
          'profile_use_background_image': user.profile_use_background_image, 
          'id': user.id, 
          'verified': user.verified, 
          'profile_sidebar_fill_color': user.profile_sidebar_fill_color, 
          'profile_text_color': user.profile_text_color, 
          'followers_count': user.followers_count, 
          'protected': user.protected, 
          'location': user.location, 
          'profile_background_color': user.profile_background_color, 
          'id_str': user.id_str, 
          'utc_offset': user.utc_offset, 
          'statuses_count': user.statuses_count, 
          'description': user.description,
          'friends_count': user.friends_count, 
          'profile_link_color': user.profile_link_color, 
          'profile_image_url': user.profile_image_url,
          'notifications': user.notifications, 
          #'show_all_inline_media': user.show_all_inline_media, 
          'geo_enabled': user.geo_enabled, 
          'profile_background_image_url': user.profile_background_image_url,
          'screen_name': user.screen_name, 
          'lang': user.lang, 
          'following': user.following, 
          'profile_background_tile': user.profile_background_tile, 
          'favourites_count': user.favourites_count, 
          'name': user.name, 
          'url': user.url, 
          'created_at': _parse_datetime (user.created_at), 
          'contributors_enabled': user.contributors_enabled, 
          'time_zone': user.time_zone, 
          'profile_sidebar_border_color': user.profile_sidebar_border_color, 
          'is_translator': user.is_translator, 
          'listed_count': user.listed_count}

def _parse_datetime (date):
  return date.strftime('%a %I:%M:%S')
