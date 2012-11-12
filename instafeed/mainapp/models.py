from django.db import models
from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField, CredentialsField

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
  refresh_token = models.CharField(max_length=255)

class TwitterAccount(Account):
  access_secret = models.CharField(max_length=255)

class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()
