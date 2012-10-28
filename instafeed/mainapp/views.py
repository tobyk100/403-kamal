from django.http import HttpResponse
from django.shortcuts import render, redirect
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import twitter_api
import models

def feed(request):
  return render(request, 'Feed.html')

def index(request):
  return signin(request)

def signup(request):
  if request.method == 'POST':
    form = EmailUserCreationForm(request.POST)
    if form.is_valid():
      message = None

      email = form.clean_email()
      password = form.clean_password2()
      form.save()

      user = authenticate(email=email, password=password)
      if (user is not None) and (user.is_active):
        login(request, user)
        message = "Registration successful"
      else:
        message = "There was an error automatically logging you in. Try <a href=\"/index/\">logging in</a> manually."
      
      # TODO: fixed the rendering once homepage is ready
      return redirect('/feed/', {'username': email, 'message': message})

  else:
    form = EmailUserCreationForm()

  return render(request, 'signup.html', {'form': form})

def signin(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if (user is not None) and (user.is_active):
      login(request, user)
      return redirect('/feed/', {'username': email})
    else:
      return render(request, 'index.html', {'username': email})
  else:
    form = EmailAuthenticationForm()

  return render(request, 'index.html', {'form': form})

#Tag needed for ajax call. May need to take this out later to protect from attacks(?)
@csrf_exempt
def twitter_request(request):
#  json = request.POST
#  if json.get('type') == 'upload':
#    twitter_api.twitter_post('accessdb', 'accessdb', json.get('message'))
  #elif json.get('type') == 'feedRequest':
    #get stuff from twitter
    return HttpResponse("Hello")
#  return HttpResponse(json)

@csrf_exempt
def facebook_request(request):
  print "got here"
  return HttpResponse("got here");
  if request.method == 'POST':
    print "recieved request to post to Facebook"
    print request.POST
  elif request.method == 'GET':
    print "recieved request to retrieve posts from Facebook"
    print request.GET
  return_dict = {'message': 'Tried to interact with fb', 'code':'200'}
  json = simplejson.dumps(return_dict)
  return HttpResponse(json)

def accounts(request):
  return render(request, 'Accounts.html')

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
  #twitter_account = TwitterAccount(user_id=
  #return render(request, 'Accounts.html')
  return HttpResponse(user.username)
