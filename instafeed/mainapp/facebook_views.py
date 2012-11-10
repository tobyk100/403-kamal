from django.http import HttpResponse
from django.shortcuts import render, redirect
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import twitter_api, facebook_api, json, models, urllib2
from models import TwitterAccount, FacebookAccount, Account

@csrf_exempt
def facebook_request(request):
  response = {}
  json_request = request.POST
  if json_request.get('type') == 'upload':
    print "posting to fb"
    response = facebook_upload(request)
    print "just posted to fb"
  elif json_request.get('type') == 'feedRequest':
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
  try:
    facebook_api.facebook_post_feed(request.POST.get('message'), fb_account.access_token)
  except urllib2.HTTPError:
    print "Error: Token is invalid"
    get_fb_url(1)
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
  
  try:
    response['success'] = 'true'
    response['updates'] = facebook_api.facebook_read_user_status_updates(fb_account.access_token)
  except urllib2.HTTPError:
    print "Error: Token is invalid"
    get_fb_url(1)
  return response

def get_fb_url(error):
  url = facebook_api.facebook_auth_url()
  if(error):
    return HttpResponse(url, status=409)
  else:
    return HttpResponse(url, status=200)

@csrf_exempt
def facebook_signin(request):
  get_fb_url(0)
  

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
