from django.db import models
from django.contrib.auth.models import User

# Account is an abstract class. FacebookAccount and TwitterAccount derive
# Account. They both inherent all the fields and methods from Account.
# To get a users account info call the get_account method with their
# user_id

class Account(models.Model):
  # Returns the users account as a python object. To access their account info
  # access the fields of the object. Returns None if account doesn't exist.
  # Example usage:
  #   acc = FacebookAccount.get_account(request.user.id)
  #   print acc.request_token
  @classmethod
  def get_account(cls, request_id):
    try:
      acc = cls.objects.filter(user_id=request_id)
    except cls.DoesNotExist:
      return None
    if len(acc) == 0: return None
    return acc[0]

  user_id = models.ForeignKey(User) # Both Twitter and FacebookAccount
                                    # inheret these fields
  access_token = models.CharField(max_length=255)

  class Meta:
    abstract = True;

class FacebookAccount(Account):
  pass

class GoogleAccount(Account):
  pass

class TwitterAccount(Account):
  access_secret = models.CharField(max_length=255)

class ScheduledUpdates(models.Model):
  # Returns the preceding updae by date ascending.
  # Example usage:
  #  update = ScheduledUpdates.objects.get(id = 5)
  #  prev = update.get_previous
  def get_previous_id(self):
    updates = ScheduledUpdates.objects.filter(user_id = self.user_id,
                                              publish_date__lt = self.publish_date)\
        .order_by("-publish_date")
    if len(updates) > 0:
      return updates[0].id
    else:
      return 0

  user_id = models.ForeignKey(User) #maps update to user
  update = models.CharField(max_length=255)
  publish_date = models.DateTimeField()
  publish_site = models.IntegerField(max_length=10) #For now it will allow us to distinguish
    #between the sites we want to post to
    #1=fb, 2=twitter, 3=both
    #We can change this later but I thought it
    #it would be a good place holder for now
