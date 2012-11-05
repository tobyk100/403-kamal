from django.http import HttpResponse
from django.shortcuts import render, redirect
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import twitter_api, facebook_api, json, models
from models import TwitterAccount, FacebookAccount, Account

@csrf_exempt
def facebook_request(request):
  response = {}
  json = request.POST
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
    return response
  
  response['success'] = 'true'
  facebook_api.facebook_post_feed(request.POST.get('message'), fb_account.access_token)
  return response

@csrf_exempt
def facebook_feed_request(request):
  response = {}
  try:
    fb_account = FacebookAccount.get_account(request.user.id)
  except Entry.DoesNotExist:
    response['success'] = 'false'
    response['message'] = 'Failed to get data for user'
    return response
  
  response['success'] = 'true'
  response['updates'] = facebook_api.facebook_read_user_status_updates(fb_account.access_token)
  return response

@csrf_exempt
def facebook_signin(request):
  print "trying to sign into facebook"
  url = facebook_api.facebook_auth_url()
  return HttpResponse(url)

@csrf_exempt
def facebook_callback(request):
  if request.GET.get('access_token') != None:
    fb_access_token = request.POST.get('access_token')
    facebook_account = FacebookAccount(user_id=request.user, access_token=fb_access_token)
    return_dict = {}
    return_dict['success'] = 'true'
    return HttpResponse(json.dumps(return_dict))
  else:
    return render(request, 'channel.html')

@csrf_exempt
def facebook_access(request):
  fb_access_token = request.POST.get('token')
  facebook_account = FacebookAccount(user_id=request.user, access_token=fb_access_token)
  facebook_account.save()
  return_dict = {}
  return_dict['success'] = 'true'
  return HttpResponse(json.dumps(return_dict))