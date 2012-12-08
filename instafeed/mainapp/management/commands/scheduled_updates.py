from django.core.management.base import BaseCommand, CommandError
from mainapp.models import TwitterAccount, FacebookAccount, Account, ScheduledUpdates
import datetime
from mainapp import twitter_api, twitter_views


class Command(BaseCommand):

  def handle(self, *args, **options):
    now = datetime.datetime.utcnow()
    #we can now call now.year, now.hour,  now.month, and now.day to figure out the exact date
    #querying the db returns datetime objects
    #TODO need to learn to query these date times correctly. For some reason giving me an error on hour
    posts = ScheduledUpdates.objects.filter(publish_date__year=now.year, \
                                            publish_date__month=now.month, \
                                            publish_date__day=now.day)
                                            #publish_date__hour=now.hour)
    
    
    for post in posts:
      print post.publish_date
      #if post.publish_site is 1 or 3:
      #  fb_account = FacebookAccount.get_account(post.user_id)
      #  facebook_api.facebook_post_feed(post.update, fb_account.access_token)
      if post.publish_site is 2 or 3 and post.publish_date.hour == now.hour:
        twitter_account = TwitterAccount.get_account(post.user_id)
        twitter_api.twitter_post(twitter_account.access_token, twitter_account.access_secret, post.update)
