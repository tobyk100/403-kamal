"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import unittest
from mainapp.models import GoogleAccount
from django.http import HttpResponse, HttpRequest
from django.test.client import Client
import json



class GoogleTest(TestCase):
  def setUp(self):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.save()

  def test_google_model(self):
    user = User.objects.get(id=1)
    account = GoogleAccount(user_id=user, access_token="test_access_token", 
        refresh_token="test_refresh_token")
    account.save()
    account = GoogleAccount.get_account(user.id)
    self.assertEqual("test_access_token", account.access_token)
    self.assertEqual("test_refresh_token", account.refresh_token)

  def test_google_signin_not_authenticated(self):
    c = Client()
    response = c.post('/google_signin/')
    json_response = json.loads(response.content)
    self.assertEqual(json_response["success"], False)
