from models import TwitterAccount, FacebookAccount, Account, ScheduledUpdates 
import datetime, twitter_views, facebook_views

def CheckForUpdates():
  now = datetime.datetime.now()
  #we can now call now.year, now.hour,  now.month, and now.day to figure out the exact date
  #querying the db returns datetime objects
  posts = ScheduledUpdates.objects.filter(
		publish_date__year=now.year,
		publish_date__month=now.month,
		publish_date__day=now.day)
  for post in posts:
    #TODO for each post that has been found for the day we need to make a twitter/facebook request	 
    if post.publish_site is 1 or 3:
      fb_account = FacebookAccount.get_account(post.user_id)
      facebook_api.facebook_post_feed(post.update, fb_account.access_token)  
    if post.publish_site is 2 or 3:
      twitter_account = TwitterAccount.get_account(post.user_id)
      twitter_api.twitter_post(twitter_account.access_token, twitter_account.access_secret, post.update)   
