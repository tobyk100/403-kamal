# This module provides google plus api interaction and 
# a main method for testing
from urllib import urlencode
from settings import DEBUG

AUTH_URL = 'https://accounts.google.com/o/oauth2/auth?'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'

if DEBUG:
  CLIENT_ID = '138535205339.apps.googleusercontent.com'
  CLIENT_SECRET = 'WumC2izjkBtsD4Dao8j_mrJ8'
  REDIRECT_URI = 'http://dry-peak-6840.herokuapp.com'
else:
  CLIENT_ID = '40247122188-8mvrgqaqh7i5d956ab8tjbu3vpt1u79m.apps.googleusercontent.com'
  CLIENT_SECRET = 'yD6qjL6j0Ybdqk8QVgo73lP9'
  REDIRECT_URI = 'http://127.0.0.1:8000'

def request_code():
  params = {}
  params['response_type'] = 'code'
  params['client_id'] = CLIENT_ID
  params['redirect_uri'] = REDIRECT_URI + '/google_callback_code'
  params['scope'] = 'https://www.googleapis.com/auth/userinfo.profile'
  url = AUTH_URL + urlencode(params)
  return url

def request_token_post(code):
  post = {}
  post['code'] = code
  post['client_id'] = CLIENT_ID
  post['client_secret'] = CLIENT_SECRET
  post['redirect_uri'] = REDIRECT_URI + '/google_callback_token'
  post['grant_type'] = 'authorization_code'
  return post

def request_token_url():
  return TOKEN_URL


if __name__ == '__main__':
  print "hi"
