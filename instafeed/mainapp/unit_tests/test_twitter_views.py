from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth import login
import datetime, json
from ..models import TwitterAccount, Account
from .. import twitter_views

class TwitterViewsTestCase(TestCase):
  def setUp(self):
    self.client = Client()

  def test_twitter_request(self):
    user = User.objects.create_user('fakename', 'fake@pukkared.com', 'mypassword')
    res = self.client.login(email='fake@pukkared.com', password='mypassword')
    self.assertEquals(res, True)
    self.assertIn('_auth_user_id', self.client.session)

    account = TwitterAccount(user_id=user,
            access_token='865080817-d425Tqu8Q1CwqHQcMLYh63RnVVoue4p97hNj6rb0',
            access_secret='2WYnZAH5FQJm6jUOhi3hpqU6oh2J4QBwWb96ORFX7g'
          )
    account.save()

    one_user = TwitterAccount.get_account(request_id=user.id)
    self.assertNotEquals(one_user, None)

    # Normal upload
    response = self.client.post('/twitter_request/', {'type': 'upload',
      'message': 'test_request ' + str(datetime.datetime.now())})
    self.assertEquals(response.status_code, 200)
    self.assertHTMLEqual(response.content, '{"success": true}')

    # More than 140 characters upload
    txt = ('test_request ' + str(datetime.datetime.now()) + ' ') * 50
    response = self.client.post('/twitter_request/', {'type': 'upload',
      'message': txt})
    self.assertEquals(response.status_code, 200)
    self.assertHTMLEqual(response.content, '{"success": false}')

    # Fetch posts
    response = self.client.post('/twitter_request/', {'type': 'feedRequest'})
    response_dict = json.loads(response.content)
    self.assertIn('success', response_dict)
    self.assertIn('tweets', response_dict)

