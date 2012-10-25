from django.db import models

class Account(models.Model):
  user_id = models.ForeignKey(User)
  access_token = models.CharField(max_length=255)
  expires = models.DateTimeField()
  
  class Meta:
    abstract = true;

class FacebookAccount(Account):

class TwitterAccount(Account):
  access_secret = models.CharField(max_length=255)
