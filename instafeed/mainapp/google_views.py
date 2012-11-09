from django.http import HttpResponse, HttpResponseRedirect
import json
import google_api
from models import GoogleAccount

"""
Main use case flows:
    1) Ask for users' posts
    2) Check session for valid token
    3) If valid, use to get posts and return
    4) If not valid or non existent check database for refresh token
    5) If refresh token, use to get access token, cache access token in session
      get posts, return
    6) If no refresh token, go to signin

    1) Ask to signin user
    2) Check for valid refresh token in database
    3) If valid refresh token then return success (user is signed in)
    4) If no valid refresh token then redirect to google
    5) if callback fails return fail
    6) if callback succeeds, put refresh token into db, get access token, cache
      access token into session.
"""

def google_signup(request):
  response = {}
  if not request.user.is_authenticated():
    response['success'] = False
    response['authenticated'] = False
    response['message'] = "User not authenticated"
    return HttpResponse(json.dumps(response))

  account = GoogleAccount.get_account(request.user)
  if account is None:
    redirect = _request_refresh_token()
    redirect['success'] = True
    redirect['authenticated'] = True
    redirect['account'] = False
    redirect['message'] = "User redirected to G+ for signin"
    return redirect

  response['refresh_token'] = account.refresh_token
  return HttpResponse(json.dumps(response))


def google_get_posts(request):
  response = {}
  token = request.session.get('google_token')
  if (token is None) or (not is_valid(token)):
    token = _request_token(request)
  return HttpResponse(json.dumps(response), 'application/json')
  return HttpResponseRedirect(url)

def _request_token(request):
  response = {}
  account = GoogleAccount.get_account(request.user)
  response['refresh_token'] = request_refresh_token(request) if not account else \
                              account.refresh_token
  return HttpResponse(json.dumps(response))

# Asks google for a code, google calls back '_google_callback_code'
# and that method handles getting the request and putting it in the DB
def _request_refresh_token():
  """
  request_post = google_api.request_token_post(request.code)
  url = request_token_url()
  redirect = HttpResponseRedirect(url)
  redirect.POST.update(request_post)
  """
  url = google_api.TOKEN_URL
  redirect = HttpResponseRedirect(url)
  return redirect

# returns a json object with the following fields:
#   authorized - A boolean representing whether the user gave us access
def _google_callback_code(request):
  response = {}
  response['authorized'] = (request.GET.get('error') != 'access_denied')
  if response['authorized']:
    response['code'] = request.GET.get('code')

  return HttpResponse(json.dumps(response))

def google_callback_token(request):
  pass
