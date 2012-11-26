from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from models import TwitterAccount, Account
import twitter_api, json

#Tag needed for ajax call. May need to take this out later to protect from attacks(?)
@csrf_exempt
def twitter_request(request):
  one_user = TwitterAccount.get_account(request_id=request.user.id)
  if one_user is None:
    return_dict = {'success' : False}
    return_json = json.dumps(return_dict)
    return HttpResponse(return_json, mimetype="application/json")
  request_json = request.POST
  if request_json.get('type') == 'upload':
    twitter_api.twitter_post(one_user.access_token, one_user.access_secret, request_json.get('message'))
    return_dict = {'success': True}
    return_post_json = json.dumps(return_dict)
    return HttpResponse(return_post_json, mimetype="application/json")
  elif request_json.get('type') == 'feedRequest':
    print "hi"
    #get stuff from twitter

    twitter_post = twitter_api.twitter_home_timeline(one_user.access_token, one_user.access_secret, 10)
    return_dict = {'tweets': twitter_post, "success": True}
    return_tweets_json = json.dumps(return_dict)
    return HttpResponse(return_tweets_json, mimetype="application/json")
  else:
    return_dict = {"success": False}
    return HttpResponse(json.dumps(return_dict), mimetype="application/json")


@csrf_exempt
def twitter_signin(request):
  t = twitter_api.twitter_authentication_url()
  if t is None:
    return_dict = {"success": False}
    return HttpResponse(json.dumps(return_dict), mimetype="application/json")
  else:
    return_dict = {"success": True}
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
  return render(request, 'Accounts.html')
