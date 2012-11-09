"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase
from django.utils import unittest
from mainapp.models import GoogleAccount
from django.http import HttpResponse, HttpRequest
from django.test.client import Client
from emailusernames.utils import create_user
import google_api
import json
import mox



class GoogleTest(TestCase):
  def setUp(self):
    self.email = 'john'
    self.password = 'johnpassword'
    user = create_user(self.email, self.password)
    self.user = user

  def tearDown(self):
    users = User.objects.all()
    users.delete()

  def addAccountToDB(self):
    user = User.objects.get(id=1)
    self.access_token = "test_access_token"
    self.refresh_token = "test_refresh_token"
    account = GoogleAccount(user_id=user, access_token=self.access_token, 
        refresh_token = self.refresh_token)
    account.save()

  def test_model(self):
    self.addAccountToDB()
    user = User.objects.get(id=1)
    account = GoogleAccount.get_account(user.id)
    self.assertEqual(self.access_token, account.access_token)
    self.assertEqual(self.refresh_token, account.refresh_token)

  def test_signup_not_authenticated(self):
    c = Client()
    response = c.post('/google_signup/')
    json_response = json.loads(response.content)
    self.assertFalse(json_response["success"])
    self.assertFalse(json_response["authenticated"])

  def test_signup_authenticated_no_account(self):
    """
    user = User.objects.get(id=1)
    c = Client()
    c.login(email=self.email, password=self.password)
    response = c.post('/google_signup/')
    json_response = json.loads(response.content)
    self.assertTrue(json_response["success"])
    self.assertTrue(json_response["authenticated"])
    self.assertFalse(json_response["account"])
    """
    response = _request_refresh_token()
    self.assertRedirects(response, google_api.TOKEN_URL)

"""
  def test_signup_authenticated_no_account(self):
    c = Client()
    c.login(email=self.email, password=self.password)
    self.addAccountToDB
    reponse = c.post('/oogle_api.request_token(request)
"""
