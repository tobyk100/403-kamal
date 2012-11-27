from models import TwitterAccount, FacebookAccount, Account, ScheduledUpdates 
import datetime

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
