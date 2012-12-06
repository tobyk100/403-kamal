from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from models import TwitterAccount, Account
import twitter_api, json

#Tag needed for ajax call. May need to take this out later to protect from attacks(?)
@csrf_exempt
def twitter_request(request):
  one_user = TwitterAccount.get_account(request_id=request.user.id)
  return_dict = {'success': False}
  if one_user is not None:
    request_json = request.POST
    if request_json.get('type') == 'upload':
      message = request_json.get('message')
      if len(message) <= 140:
        twitter_api.twitter_post(
            one_user.access_token,
            one_user.access_secret,
            message
        )
        return_dict['success'] = True
    elif request_json.get('type') == 'feedRequest':
      twitter_post = twitter_api.twitter_home_timeline(
          one_user.access_token,
          one_user.access_secret,
          30
      )
      return_dict['tweets'] = twitter_post
      return_dict['success'] = True
    elif request_json.get('type') == 'retweet':
      postId = request_json.get('postId')
      success = twitter_api.twitter_retweet(
          one_user.access_token,
          one_user.access_secret,
          postId
      )
      return_dict['success'] = success
  return_json = json.dumps(return_dict)
  return HttpResponse(return_json, mimetype="application/json")


@csrf_exempt
def twitter_signin(request):
  t = twitter_api.twitter_authentication_url()
  request.session['request_token'] = t[1]
  request.session['request_secret'] = t[2]
  return HttpResponse(t[0])

#need to test this
def twitter_callback(request):
  verifier = request.GET.get('oauth_verifier')
  token_info = twitter_api.twitter_authenticate(verifier, request.session['request_token'], request.session['request_secret'])
  user = request.user
  if user:
    twitter_account = TwitterAccount(user_id=user, access_token=token_info[0], access_secret=token_info[1])
    twitter_account.save()
  return HttpResponseRedirect('/feed/')
