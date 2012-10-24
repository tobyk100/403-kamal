from django.http import HttpResponse
from django.shortcuts import render
from emailusernames.forms import EmailUserCreationForm
from django.contrib.auth import authenticate, login

def index(request):
  return render(request, 'index.html')

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
      return render(request, 'index.html', {'username': email, 'message': message})

  else:
    form = EmailUserCreationForm()

  return render(request, 'signup.html', {'form': form})
  
def twitter_request(request):
  if request.method == 'POST':
    print "recieved request to post to Twitter"
    print request.POST
  elif request.method = 'GET':
    print "recieved request to retrieve posts from Twitter"
    print request.GET
  return HttpResponse()

def facebook_request(request):
  if request.method == 'POST':
    print "recieved request to post to Facebook"
    print request.POST
  elif request.method = 'GET':
    print "recieved request to retrieve posts from Facebook"
    print request.GET
  return HttpResponse()