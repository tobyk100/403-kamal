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
    #redirect = request_refresh_token(request)
    response['success'] = True
    response['authenticated'] = True
    response['account'] = False
    response['message'] = "User redirected to G+ for signin"
    return HttpResponse(json.dumps(response))

  response['refresh_token'] = account.refresh_token
  return HttpResponse(json.dumps(response))


def google_get_posts(request):
  response = {}
  token = request.session.get('google_token')
  if (token is None) or (not is_valid(token)):
    token = google_api.google_request_token(request)

  return HttpResponse(json.dumps(response), 'application/json')

  return HttpResponseRedirect(url)
