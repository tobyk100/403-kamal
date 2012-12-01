#!/usr/bin/env python
import facebook_lib as F
import urllib2
import datetime
import json
#Facebook moduel for InstaFeed.
#Example usage can be found at bottom in main

#Posts a message to facebook(update your own status)
def facebook_post_feed(post, access_token):
  F.ACCESS_TOKEN = access_token
  F.graph_post('/me/feed', {'message': post})

#Gets posts on a users news feed.
#Returns a list of tuples:
#tuple form: (message, name, time)
#time is currently expressed as a unix timestamp(number of seconds since Jan1 1970)
def facebook_read_user_status_updates(access_token):
  posts = []
  F.ACCESS_TOKEN = access_token
  queries = {}

  queries['query1'] = "SELECT filter_key FROM stream_filter WHERE uid=me() AND type='newsfeed'"

  queries['query2'] = "SELECT post_id, actor_id, target_id, message, created_time FROM stream WHERE filter_key in (SELECT filter_key FROM #query1) AND is_hidden = 0"

  queries['query3'] = "SELECT first_name, last_name, uid FROM user WHERE uid IN (SELECT actor_id FROM #query2)"

  results = F.fql_multiquery(queries);
  query1 = results[1]['fql_result_set'];
  query2 = results[2]['fql_result_set'];

  for post in query1:
    message = post['message'].encode('utf-8')
    created_time = post['created_time']
    actor_id = str(post['actor_id'])
    if((actor_id != None) and (message != "")):
      first_name = ""
      last_name = ""
      name = ""
      for entry in query2:
        #look for user_id in query2 to get name
        if entry['uid'] == post['actor_id']:
          first_name = entry['first_name']
          last_name = entry['last_name']
          break
      name = first_name + " " + last_name
      time = str(created_time)
      image = "https://graph.facebook.com/" + str(post['actor_id']) + "/picture"
      image1 = urllib2.urlopen(image);
      image2 = image1.geturl();
      post_id = post['post_id']
      if(name != " "):
        posts.append((message, name, time, image2, post_id))
  return posts

  """
  graph_path = '/me/home'
  graph_res = F.graph(graph_path)
  for d in graph_res['data']:
    name = d['from']['name']
    time = d['created_time']
    message = d['message']
    post_id = d['id']
    image_src = F.graph(d['from']['id'] + '/picture')['data']['url']
    posts.append((message, name, time, image_src, post_id))
  """

#This function will open a web browser with the page the user needs to log in to.
#It will parse out the 'access_token' and return it.
#This function seems to fail if the user is already logged in to Facebook.
#Using the auth function below is likely better for including the Facebook
#moduel into InstaFeed, but this method is useful to debug this moduel or see
#it in action.
def facebook_auth():
  F.AUTH_SCOPE = ['publish_stream', 'read_stream', 'user_status', 'offline_access']
  return F.authenticate()

#Returns the url the user needs to be redirected to to log into Facebook.
#If you use this function, front end will have to handle the redirect and
#parse out the returned 'access_token'
def facebook_auth_url():
  F.AUTH_SCOPE = ['publish_stream', 'read_stream', 'user_status', 'offline_access']
  return F.get_auth_url()

#Likes a post on facebook.
#Params: The post_id of the post you want to like, and a valid access token
def facebook_like_post(post_id, access_token):
  post_url = '/' + post_id + '/likes/'
  params = {'access_token' : access_token}
  F.graph_post(post_url, params)


#Comment on a facebook post
#Params: The post_id of the post you want to comment on, the comment you want to post, and a valid access token
def facebook_comment_post(post_id, comment, access_token):
  post_url = '/' + post_id + '/comments/'
  params = {'access_token' : access_token, 'message' : comment}
  F.graph_post(post_url, params)


#Example of how to use facebook_api.py:
#Run 'python facebook_api.py'
#This script will update your status and print some recent posts from your news feed.
#Make sure you are logged out of Facebook or the get access_token will fail
def main():
  #Log in to facebook to get your access token
# access_token = facebook_auth()
  access_token = 'AAACEdEose0cBAPIcbq4Uzw5LQprCIwdA30VtOkk1bhjFG4I8E4cgyKJM0CaZCCizQtSDIwc6x2xmeORHojXQDKQeDZAFKZA4ZBS3OZBfTX7rAN3ZAeM6hG'

  #Update your status
  post = "Postinadsfg from InstaFeed!adsawwdsfadxsfa"
#  facebook_post_feed(post, access_token);

  #View your news feed
  posts = facebook_read_user_status_updates(access_token);

  #Like the first post!
  post_id = posts[0][4];
  facebook_like_post(post_id, access_token);

  #Comment on the post!
  comment = "COMMENTING FROM INSTAFEED!!!"
  facebook_comment_post(post_id, comment, access_token);

  #Print the posts out
  for post in posts:
    print "--- Next Post ---"
    print "message: " + post[0]
    print "name: " + post[1]
    print "timestamp: " + post[2]
    print "image: " + post[3]
    print "post_id" + post[4]
    print ""

#for debugging
if __name__ == "__main__":
  main()
