import datetime
from django.test import TestCase
from datetime import timedelta
from .. import twitter_api


class TwitterApiTestCase(TestCase):
  def test_parse_datetime(self):
    d = datetime.datetime(2012, 8, 4, 12, 30, 45)
    d2 = datetime.datetime(2012, 12, 4, 0, 0, 0)
    self.assertEquals(twitter_api._parse_datetime(d), 
                     (d - timedelta(hours=8)).strftime('%a %I:%M:%S'))
    self.assertEquals(twitter_api._parse_datetime(d2),
                     (d2 - timedelta(hours=8)).strftime('%a %I:%M:%S'))
