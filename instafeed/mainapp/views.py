from django.http import HttpResponse
from django.shortcuts import render
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

def feed(request):
  return render(request, 'Feed.html')

def index(request):
  form = EmailAuthenticationForm()
  return render(request, 'index.html', {'form': form})

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

def login(request):
      email = request.POST['email']
      email = request.POST['password']
      user = authenticate(email=email, password=password)
      if (user is not None) and (user.is_active):
        login(request, user)
        return render(request, 'index.html', {'username': email})
      else:
        return render(request, 'index.html', {'username': email})

#Tag needed for ajax call. May need to take this out later to protect from attacks(?)
@csrf_exempt
def twitter_request(request):
  if request.method == 'POST':
    print "recieved request to post to Twitter"
    print request.POST
  elif request.method == 'GET':
    print "recieved request to retrieve posts from Twitter"
    print request.GET
  return_dict = {'message': 'Tried to interact with twitter', 'code':'200'}
  json = simplejson.dumps(return_dict)
  return HttpResponse(json)

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
  render(request, 'Accounts.html');

