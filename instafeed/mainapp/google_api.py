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

def google_request_token(request):
  account = GoogleAccount.get_account(request.user)
  refresh_token = request_refresh_token(request) if not account else \
                  account.refresh_token

def request_refresh_token(request):
  request_post = google_api.request_token_post(request.code)
  url = request_token_url()
  redirect = HttpResponseRedirect(url)
  redirect.POST.update(request_post)

  return redirect

# returns a json object with the following fields:
#   authorized - A boolean representing whether the user gave us access
def google_callback_code(request):
  response = {}
  response['authorized'] = (request.GET.get('error') != 'access_denied')
  if response['authorized']:
    response['code'] = request.GET.get('code')

  return HttpResponse(json.dumps(response))

def google_callback_token(request):
  pass
