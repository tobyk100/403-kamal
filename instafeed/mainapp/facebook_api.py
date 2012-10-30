#!/usr/bin/env python
import facebook_lib as F

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

		if(post['actor_id'] != None):
			name_query = "SELECT first_name, last_name FROM user WHERE uid =" + str(post['actor_id'])
			names = F.fql(name_query)
			name = ""
			if(len(names) > 0):
				names = names[0]
				first_name = names['first_name']
				last_name = names['last_name']
				name = first_name + " " + last_name
			time =  str(created_time)
			posts.append((message, name, time))
	return posts	

#This function will open a web browser with the page the user needs to log in to.
#It will parse out the 'access_token' and return it.
#This function seems to fail if the user is already logged in to Facebook.
#Using the auth function below is likely better for including the Facebook
#moduel into InstaFeed, but this method is useful to debug this moduel or see
#it in action. 
def facebook_auth():
	F.AUTH_SCOPE = ['publish_stream', 'read_stream', 'user_status']
	return F.authenticate()

#Returns the url the user needs to be redirected to to log into Facebook.
#If you use this function, front end will have to handle the redirect and 
#parse out the returned 'access_token'
def facebook_auth_url():
	F.AUTH_SCOPE = ['publish_stream', 'read_stream', 'user_status']
	return F.get_auth_url()

#Example of how to use facebook_api.py:
#Run 'python facebook_api.py' 
#This script will update your status and print some recent posts from your news feed.
#Make sure you are logged out of Facebook or the get access_token will fail
def main():
	#Log in to facebook to get your access token
	access_token = facebook_auth()

	#Update your status
	post = "Posting from InstaFeed!"
	facebook_post_feed(post, access_token);

	#View your news feed
	posts = facebook_read_user_status_updates(access_token);

	#print the posts out!
	for post in posts:
		print "--- Next Post ---"
		print "message: " + post[0]
		print "name: " + post[1]
		print "timestamp: " + post[2]
		print ""
#for debugging
if __name__ == "__main__":	
	main()
