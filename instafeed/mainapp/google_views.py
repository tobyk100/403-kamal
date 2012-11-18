from django.http import HttpResponse, HttpResponseRedirect, \
    HttpRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json
import google_api as api
from models import GoogleAccount
import requests
import time

@csrf_exempt
def google_signup(request):
  response = {}
  if not request.user.is_authenticated():
    response['success'] = False
    response['authenticated'] = False
    response['message'] = "No user signed in"
    return HttpResponseServerError(json.dumps(response))

  account = GoogleAccount.get_account(request.user)
  if account is None:
    redirect = request_code(request)
    redirect['success'] = True
    redirect['authenticated'] = True
    redirect['account'] = False
    redirect['message'] = "User redirected to G+ for signin"
    return redirect

  response['success'] = False
  response['authenticated'] = True
  response['account'] = True
  response['message'] = "User already signed up for G+"
  return HttpResponseServerError(json.dumps(response))

@csrf_exempt
def google_get_posts(request):
  response = {}
  token = request.session.get('google_token')
  if token is None or not is_token_valid(request):
    response = request_token(request)
    token = request.session.get('google_token')
  response = requests.get(api.ACTIVITY_URL, params={'access_token': token})
  posts = json.loads(response.text)
  items = posts.get('items')
  return HttpResponse(json.dumps(package_items(items)))

def package_items(items):
  packaged_items = []
  if items is not None:
    for i in items:
      packaged_items.append({
          "author_display_name": i['actor']['displayName'],
          "author_account_url": i['actor']['url'],
          "author_image_url": i['actor']['image']['url'],
          "published": i['published'],
          "updated": i['updated'],
          "content": i['object']['content'],
          "url": i['url']
      })
  return packaged_items


def is_token_valid(request):
  return request.session.get('google_token_expires') > time.time()

# Only works if user has successfully signed up
def request_token(request):
  account = GoogleAccount.get_account(request.user.id)
  response = {}
  if not account:
    response['success'] = False
    response['account'] = False
    response['message'] = "No g+ account for user, call google_signup"
    return response
  refresh_token = account.access_token # really is refresh token
  post = api.request_token(refresh_token)
  r_json = json.loads(requests.post(api.TOKEN_URL, data = post).text)
  request.session['google_token'] = r_json['access_token']
  request.session['google_token_expires'] = r_json['expires_in'] + time.time()
  response['success'] = True
  response['account'] = True
  response['message'] = "Access token stored in session"
  return HttpResponse(json.dumps(response))

# Asks google for a code, google calls back 'google_callback_code'
# and that method handles getting the request and putting it in the DB
def request_refresh_token(code):
  post = api.request_refresh_post(code)
  print "request_refresh " + str(post)
  r = requests.post(api.TOKEN_URL, data = post)
  print "response " + str(r)
  refresh_token = json.loads(r.text)['refresh_token']
  print "refresh_token " + str(refresh_token)
  return refresh_token

def request_code(request):
  url = api.request_code()
  return HttpResponse(url)

# returns a json object with the following fields:
#   authorized - A boolean representing whether the user gave us access
def google_callback_code(request):
  response = {}
  response['authorized'] = (request.GET.get('error') != 'access_denied')
  if response['authorized']:
    response['code'] = request.GET.get('code')
  print "Call back from google: " + response['code']
  refresh_token = request_refresh_token(response['code'])
  print "Refresh token in callback_code: " + refresh_token
  account = GoogleAccount(user_id=request.user,
                          access_token=refresh_token)
  account.save()
  return HttpResponseRedirect('/accounts/')
