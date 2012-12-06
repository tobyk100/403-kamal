import datetime
from django.test import TestCase
from datetime import timedelta
from .. import twitter_api


class TwitterApiTestCase(TestCase):
  def setUp(self):
    self.access_token = 'd425Tqu8Q1CwqHQcMLYh63RnVVoue4p97hNj6rb0'
    self.access_secret = '2WYnZAH5FQJm6jUOhi3hpqU6oh2J4QBwWb96ORFX7g'

  def test_twitter_authentication_url(self):
    auth_url, key, secret = twitter_api.twitter_authentication_url()
    self.assertNotEquals(auth_url, None)
    self.assertNotEquals(key, None)
    self.assertNotEquals(secret, None)

  def twitter_retweet(self):
    res = self.client.login(email='fake@pukkared.com', password='mypassword')
    self.assertEquals(res, True)
    res = twitter_api.twitter_retweet(
            self.access_token,
            self.access_secret,
            269891703756955649
          )
    self.assertEquals(res, True)

  def test_parse_datetime(self):
    d = datetime.datetime(2012, 8, 4, 12, 30, 45)
    d2 = datetime.datetime(2012, 12, 4, 0, 0, 0)
    self.assertEquals(twitter_api._parse_datetime(d),
                     (d - timedelta(hours=8)).strftime('%a %I:%M:%S'))
    self.assertEquals(twitter_api._parse_datetime(d2),
                     (d2 - timedelta(hours=8)).strftime('%a %I:%M:%S'))
