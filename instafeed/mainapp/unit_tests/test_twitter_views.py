from django.test import TestCase
from django.test.client import Client
from .. import twitter_views

class TwitterViewsTestCase(TestCase):
  def setUp(self):
    self.client = Client()

  def test_request(self):
    response = self.client.get('/twitter_request/')
    self.assertEquals(response.status_code, 200)
    self.assertEquals(response.content, '{"success": false}')
