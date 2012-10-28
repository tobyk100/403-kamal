from django.db import models
from django.contrib.auth.models import User

# Account is an abstract class. FacebookAccount and TwitterAccount derive
# Account. They both inherent all the fields and methods from Account.
#
class Account(models.Model):
  user_id = models.ForeignKey(User) # Both Twitter and FacebookAccount
                                    # inheret these fields
  access_token = models.CharField(max_length=255)
  
  class Meta:
    abstract = True;

class FacebookAccount(Account):
  expires = models.DateTimeField()

class TwitterAccount(Account):
  access_secret = models.CharField(max_length=255)
  expires = models.DateTimeField()
