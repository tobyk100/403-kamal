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
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.test.client import Client
from emailusernames.utils import create_user
import google_api
import json
import mox



class GoogleTest(TestCase):
  def setUp(self):
    pass

  def test_google_signup(self):
    response = self.client.get('/google_signup/', follow=True)
    test_uri = "https://accounts.google.com/o/oauth2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fgoogle_callback_token&response_type=code&client_id=40247122188-8mvrgqaqh7i5d956ab8tjbu3vpt1u79m.apps.googleusercontent.com&access_type=offline"
    self.assertRedirects(response, test_uri, target_status_code=404)
