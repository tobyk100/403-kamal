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
    return HttpResponseServerError(json.dumps(response), mimetype="application/json")

  redirect = request_code(request)
  return redirect

@csrf_exempt
def google_get_posts(request):
  response = {}
  token = request.session.get('google_token')
  if token is None or is_token_expired(request):
    r = request_token(request)
    r_json = json.loads(r.content)
    if r_json['success'] == False:
      # Request token failed, fail
      return HttpResponse(json.dumps(r_json), mimetype="application/json")
    token = request.session.get('google_token')
  r = requests.get(api.ACTIVITY_URL, params={'access_token': token})
  r_json = json.loads(r.text)
  if r_json.get('error') is not None:
    return HttpResponse(json.dumps(r_json), mimetype="application/json")
  items = r_json.get('items')
  response['posts'] = package_items(items)
  response['success'] = True
  response['account'] = True
  return HttpResponse(json.dumps(response), mimetype="application/json")

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


def is_token_expired(request):
  return request.session.get('google_token_expires') < time.time()

# Only works if user has successfully signed up
def request_token(request):
  account = GoogleAccount.get_account(request.user.id)
  response = {}
  if not account:
    response['success'] = False
    response['account'] = False
    response['message'] = "No g+ account for user, call google_signup"
    return HttpResponse(json.dumps(response), mimetype="application/json")
  refresh_token = account.access_token # really is refresh token
  post = api.request_token(refresh_token)
  r = (requests.post(api.TOKEN_URL, data = post).text)
  r_json = json.loads(r)
  if (r_json.get('error') is not None):
    response['success'] = False
    response['account'] = True
    response['message'] = "Google + rejected your credentials"
  else:
    request.session['google_token'] = r_json['access_token']
    request.session['google_token_expires'] = r_json['expires_in'] + time.time()
    response['success'] = True
    response['account'] = True
    response['message'] = "Access token stored in session"
  return HttpResponse(json.dumps(response), mimetype="application/json")

# Asks google for a code, google calls back 'google_callback_code'
# and that method handles getting the request and putting it in the DB
def request_refresh_token(code):
  post = api.request_refresh_post(code)
  r = requests.post(api.TOKEN_URL, data = post)
  refresh_token = json.loads(r.text)['refresh_token']
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
    refresh_token = request_refresh_token(response['code'])
    account = GoogleAccount(user_id=request.user,
                            access_token=refresh_token)
    account.save()
  return HttpResponseRedirect('/feed/')
