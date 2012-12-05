from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.test.client import Client

class ViewsTestCase(TestCase):
  def setUp(self):
    self.client = Client()

  def test_index(self):
    response = self.client.get('/')
    self.assertEquals(response.status_code, 302)
    self.assertRedirects(response, '/signin/?next=/')

    User.objects.create_user('fakename', 'fake@pukkared.com', 'mypassword')
    res = self.client.login(email='fake@pukkared.com', password='mypassword')
    self.assertEquals(res, True)
    self.assertIn('_auth_user_id', self.client.session)
    response = self.client.post('/accounts/')
    self.assertEquals(response.status_code, 200)
