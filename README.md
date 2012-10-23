403-kamal
=========

A private repo for our group.

================================
Views needed by front end javascript

Posting to Twitter:
//Javascript sends up message
//Returns nothin

Posting to Facebook:
//Javascript sends up message
//Returns nothing

Load Feeds from Twitter:
//Javascript sends up nothing
//Returns JSON object containing list of posts
//	   each with a message, author and date/time

Load Feeds from Facebook:
//Javascript sends up nothing
//Return JSON object containing list of posts
//	 each with a message, author and date/time
=======
Internal API:

Sign in:
method: POST
param: email, password, remember me
result: authenticated users, set cookies, redirect to home page (with posts)

Sign up:
method: POST
param: email, password, remember me
result: authenticate users, create a user, set cookies, redirect to home page (with posts)

