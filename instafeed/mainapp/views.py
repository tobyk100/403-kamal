from django.http import HttpResponse
from django.shortcuts import render, redirect
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from models import TwitterAccount, FacebookAccount, Account

@login_required
def feed(request):
  return render(request, 'Feed.html')

@login_required
def index(request):
  return feed(request)

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

      # Since user does not have any accounts by the time they signe in,
      # we should redirect them to accounts page instead of feed page.
      return redirect('/accounts/')

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
      facebook_account = FacebookAccount.get_account(request_id=request.user.id)
      twitter_account = TwitterAccount.get_account(request_id=request.user.id)
      if facebook_account is None and twitter_account is None:
        return redirect('/accounts/')
      else:
        return redirect('/feed/', {'username': email})
    else:
      form = EmailAuthenticationForm()
      form.non_field_errors = 'Your email and password were incorrect.'
      return render(request, 'index.html', {'form': form})
  else:
    form = EmailAuthenticationForm()

  return render(request, 'index.html', {'form': form})

def faq_request(request):
  return render(request, 'faq.html')

@login_required
def settings(request):
  return render(request, 'settings.html')

@login_required
def logoutuser(request):
  logout(request)
  return redirect('/')

@login_required
def accounts(request):
  return render(request, 'Accounts.html')

