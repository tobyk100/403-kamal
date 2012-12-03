import datetime
from datetime import timedelta
from .. import twitter_api

def test__parse_datetime():
  d = datetime.datetime(2012, 8, 4, 12, 30, 45)
  d2 = datetime.datetime(2012, 12, 4, 0, 0, 0)
  assert twitter_api._parse_datetime(d) == \
      (d - timedelta(hours=8)).strftime('%a %I:%M:%S')
  assert twitter_api._parse_datetime(d2) == \
      (d2 - timedelta(hours=8)).strftime('%a %I:%M:%S')
