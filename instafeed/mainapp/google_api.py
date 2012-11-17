# This module provides google plus api interaction and 
# a main method for testing
from urllib import urlencode, quote
<<<<<<< HEAD
from settings import DEBUG
=======
from settings import DEBUG, LOCAL
>>>>>>> 8f644160f3a68f3418ac16819ddcba564ad903e5
from models import GoogleAccount
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth?'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
ACTIVITY_URL = 'https://www.googleapis.com/plus/v1/people/me/activities/public'
SCOPE = "https://www.googleapis.com/auth/plus.me"

<<<<<<< HEAD
if DEBUG:
=======
if LOCAL:
>>>>>>> 8f644160f3a68f3418ac16819ddcba564ad903e5
  CLIENT_ID = '40247122188-8mvrgqaqh7i5d956ab8tjbu3vpt1u79m.apps.googleusercontent.com'
  CLIENT_SECRET = 'WumC2izjkBtsD4Dao8j_mrJ8'
  REDIRECT_URI = 'http://127.0.0.1:8000'
  TEST_CODE = "test_code"
  TEST_REFRESH_TOKEN = "test_refresh_token"
  TEST_TOKEN = "test_token"
else:
  CLIENT_ID = '138535205339.apps.googleusercontent.com'
  CLIENT_SECRET = 'yD6qjL6j0Ybdqk8QVgo73lP9'
  REDIRECT_URI = 'http://dry-peak-6840.herokuapp.com'

def request_code():
  params = {}
  params['response_type'] = 'code'
  params['client_id'] = CLIENT_ID
  params['redirect_uri'] = REDIRECT_URI + '/google_callback_code'
  params['scope'] = SCOPE
  params['access_type'] = 'offline'
  params['state'] = 'code'
  params['approval_prompt'] = 'force'
  url = AUTH_URL + urlencode(params)
  return url

def request_refresh_token(code):
  post = {}
  post['code'] = code
  post['client_id'] = CLIENT_ID
  post['client_secret'] = CLIENT_SECRET
  post['redirect_uri'] = REDIRECT_URI + '/google_callback_code'
  post['grant_type'] = 'authorization_code'
  return post

def request_token(refresh_token):
  post = {}
  post['refresh_token'] = refresh_token
  post['client_id'] = CLIENT_ID
  post['client_secret'] = CLIENT_SECRET
  post['grant_type'] = 'refresh_token'
  return post
