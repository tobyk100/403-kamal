from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.test.client import Client

class ViewsTestCase(TestCase):
  def setUp(self):
    self.client = Client()

  def test_index(self):
    response = self.client.get('/')
    self.assertEquals(response.status_code, 302)
    self.assertRedirects(response, '/signin/?next=/')

