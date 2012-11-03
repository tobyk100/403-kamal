from django.db import models
from django.contrib.auth.models import User

# Account is an abstract class. FacebookAccount and TwitterAccount derive
# Account. They both inherent all the fields and methods from Account.
# To get a users account info call the get_account method with their 
# user_id

class Account(models.Model):
  # Returns the users account as a python object. To access their account info
  # access the fields of the object.
  # Example usage:
  #   acc = FacebookAccount.get_account(request.user.id)
  #   print acc.request_token
  # Raises an Entry.DoesNotExist exception if their account is not found.
  def get_account(request_id):
    try:
      acc = self.objects.get(user_id=request_id)
    except DoesNotExist:
      return None
    return acc

  user_id = models.ForeignKey(User) # Both Twitter and FacebookAccount
                                    # inheret these fields
  access_token = models.CharField(max_length=255)
  
  class Meta:
    abstract = True;

class FacebookAccount(Account):
  pass

class TwitterAccount(Account):
  access_secret = models.CharField(max_length=255)
