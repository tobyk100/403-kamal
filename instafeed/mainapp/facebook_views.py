from django.http import HttpResponse
from django.shortcuts import render, redirect
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import twitter_api, facebook_api, json, models

@csrf_exempt
def facebook_request(request):
  response = {}
  json = request.POST
  post_text = json.get(message)
  if json.get('type') == 'upload':
    response = facebook_upload(request)
  elif json.get('type') == 'feedRequest':
    response = facebook_feed_request(request)
  else:
    response['success'] = 'false'
    response['message'] = 'Uknown facebook request.'
  return HttpResponse(json.dumps(response), mimetype="application/json")

@csrf_exempt
def facebook_upload(request):
  response = {}
  try:
    fb_account = FacebookAccount.get_account(request.user.id)
  except Entry.DoesNotExist:
    response['success'] = 'false'
    response['message'] = 'Failed to get data for user'
  else:
    response['success'] = 'true'
    
  facebook_api.facebook_post_feed(request.message, fb_account.access_token)
  return response

@csrf_exempt
def facebook_feed_request(request):
  response = {}
  try:
    fb_account = FacebookAccount.get_account(request.user.id)
  except Entry.DoesNotExist:
    response['success'] = 'false'
    response['message'] = 'Failed to get data for user'
  else:
    response['success'] = 'true'
    response['updates'] =  \
        facebook_api.facebook_read_user_status_updates(fb_account.access_token)
  return response

@csrf_exempt
def facebook_signin(request):
  #TODO: flesh out facebook sign in, add tokens to database
  facebook_api.facebook_auth()

@csrf_exempt
def facebook_callback(request):
  access_token = request.GET.get('access_token')
  expires_in = request.GET.get('expires_in')
