from django.test import TestCase
from django.test import Client
import json

class GoogleViewTestCase(TestCase):

  def setUp(self):
    self.client = Client()

  def test_signup(self):
    response = self.client.get('/google_signin/')
    content = json.loads(response.content)
    self.assertFalse(content['success'])
    self.assertEquals(content['message'], "No user signed in")
    self.assertEquals(response.status_code, 500)
