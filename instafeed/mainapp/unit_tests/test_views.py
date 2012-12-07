from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.test.client import Client

class ViewsTestCase(TestCase):
  def setUp(self):
    self.client = Client()

  def test_index_signin_logout(self):
    response = self.client.get('/')
    self.assertEquals(response.status_code, 302)
    self.assertRedirects(response, '/signin/?next=/')

    User.objects.create_user('fakename', 'fake@pukkared.com', 'mypassword')
    res = self.client.login(email='fake@pukkared.com', password='mypassword')
    self.assertEquals(res, True)
    self.assertIn('_auth_user_id', self.client.session)
    response = self.client.post('/feed/')
    self.assertEquals(response.status_code, 200)
    response = self.client.post('/logout/')
    self.assertEquals(response.status_code, 302)

  def test_feed(self):
    response = self.client.post('/feed/')
    self.assertEquals(response.status_code, 302)

  def test_signup(self):
    response = self.client.get('/signup/')
    self.assertEquals(response.status_code, 200)
    self.assertContains(response,
                        "<title>Instafeed</title>",
                        status_code=200)
    self.assertContains(response,
                        "<h1><a href=\"/\">Instafeed</a></h1>",
                        status_code=200)

  def test_faq_request(self):
    response = self.client.get('/faq/')
    self.assertEquals(response.status_code, 200)
    self.assertContains(response,
                        "<title>Instafeed</title>",
                        status_code=200)
    self.assertContains(response,
                        "<h1>FAQ</h1>",
                        status_code=200)
