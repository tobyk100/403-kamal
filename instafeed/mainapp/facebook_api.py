#!/usr/bin/env python
import facebook_lib as F
import urllib2
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
  query = "SELECT post_id, actor_id, target_id, message, created_time FROM stream WHERE filter_key in (SELECT filter_key FROM stream_filter WHERE uid=me() AND type='newsfeed') AND is_hidden = 0"
  for post in F.fql(query):
    message =  post['message'].encode('utf-8')
    created_time = post['created_time']
    actor_id = str(post['actor_id'])

    if((post['actor_id'] != None) and(message != '')):
      name_query = "SELECT first_name, last_name FROM user WHERE uid =" + actor_id
      names = F.fql(name_query)
      name = ""
      if(len(names) > 0):
        names = names[0]
        first_name = names['first_name']
        last_name = names['last_name']
        name = first_name + " " + last_name
      else:
        page_query = "SELECT name FROM page WHERE page_id = " + actor_id
        res = F.fql(page_query)
        if (len(res) > 0): name = res[0][u'name']
      time =  str(created_time)
      image = "https://graph.facebook.com/" + str(post['actor_id']) + "/picture"
      image1 = urllib2.urlopen(image);
      image2 = image1.geturl();
      post_id = post['post_id']
      posts.append((message, name, time, image2, post_id))
  return posts

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

  access_token = 'AAACEdEose0cBACe6ZCZCYYgQ88RBDeP3Y9TZBkRpahEOXO6M89ffPmzvp5hxtU3T6W9mBZCxySdDv9SbhXk4ZBmIoOynvITSwzOAFX0kA9MQSIZBmmQnHk'

  #Update your status
  post = "Posting from InstaFeed!adsfadsfa"
# facebook_post_feed(post, access_token);

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
