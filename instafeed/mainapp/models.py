from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
  user_id = models.ForeignKey(User)
  access_token = models.CharField(max_length=255)
  
  class Meta:
    abstract = True;

class FacebookAccount(Account):
  expires = models.DateTimeField()

class TwitterAccount(Account):
  access_token = models.CharField(max_length=255)
  access_secret = models.CharField(max_length=255)
  expires = models.DateTimeField()
