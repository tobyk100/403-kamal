from django.test import TestCase
from django.test.client import Client
from .. import models
import datetime
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from emailusernames.utils import create_user
from django.utils import timezone

class SchedulerTestCase(TestCase):
  def setUp(self):
    user = create_user(email="test@gmail.com", password="secret")
    self.when = datetime.datetime(2012, 12, 6, 22, 4, 5, 6, timezone.utc)
    new = models.ScheduledUpdates.objects.create(user_id = user,
                                           update = "hey",
                                           publish_date = self.when,
                                           publish_site = 3)
    print new.publish_date.hour

  def test_request(self):
    events = models.ScheduledUpdates.objects.filter(
        publish_date__year = self.when.year,
        publish_date__month = self.when.month,
        publish_date__day = self.when.day)
#        publish_date__time = self.when.hour)
    self.assertTrue(events.count(), 1)
    now = datetime.datetime.utcnow()
    print events[0].publish_date
    print now
    print events[0].publish_date.hour == now.hour
