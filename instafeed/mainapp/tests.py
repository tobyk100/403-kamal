from django.utils import unittest
from unit_tests import test_twitter_views, test_twitter_api, test_views, test_scheduler

def suite():
  suite = unittest.TestSuite()
  """suite.addTest(unittest.TestLoader().
      loadTestsFromTestCase(test_twitter_views.TwitterViewsTestCase))
  suite.addTest(unittest.TestLoader().
      loadTestsFromTestCase(test_twitter_api.TwitterApiTestCase))
  suite.addTest(unittest.TestLoader().
      loadTestsFromTestCase(test_views.ViewsTestCase))
    """
  suite.addTest(unittest.TestLoader().
      loadTestsFromTestCase(test_scheduler.SchedulerTestCase))
  return suite
