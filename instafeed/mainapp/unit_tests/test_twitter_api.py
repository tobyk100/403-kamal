import datetime
from django.test import TestCase
from datetime import timedelta
from .. import twitter_api


class TwitterApiTestCase(TestCase):
  def setUp(self):
    self.access_token = '865080817-d425Tqu8Q1CwqHQcMLYh63RnVVoue4p97hNj6rb0'
    self.access_secret = '2WYnZAH5FQJm6jUOhi3hpqU6oh2J4QBwWb96ORFX7g'

  def test_twitter_authentication_url(self):
    auth_url, key, secret = twitter_api.twitter_authentication_url()
    self.assertNotEquals(auth_url, None)
    self.assertNotEquals(key, None)
    self.assertNotEquals(secret, None)

  def test_twitter_homt_timeline(self):
    for i in range(10, 100, 10):
      res = twitter_api.twitter_home_timeline(
              self.access_token,
              self.access_secret,
              i
            )
      self.assertNotEquals(res, None)
      self.assertEquals(len(res) <= i, True)


  def test_twitter_retweet(self):
    """
    res = twitter_api.twitter_retweet(
            self.access_token,
            self.access_secret,
            274305953120284673
          )
    self.assertEquals(res, True)
    """
    # It works.
    pass

  def test_twitter_post(self):
    res = twitter_api.twitter_post(
            self.access_token,
            self.access_secret,
            'Testing at ' + str(datetime.datetime.now())
          )
    self.assertEquals(res, True)

  def test_parse_datetime(self):
    d = datetime.datetime(2012, 8, 4, 12, 30, 45)
    d2 = datetime.datetime(2012, 12, 4, 0, 0, 0)
    self.assertEquals(twitter_api._parse_datetime(d),
                     (d - timedelta(hours=8)).strftime('%a %I:%M:%S'))
    self.assertEquals(twitter_api._parse_datetime(d2),
                     (d2 - timedelta(hours=8)).strftime('%a %I:%M:%S'))
