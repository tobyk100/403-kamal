from django.http import HttpResponse
from django.shortcuts import render, redirect
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from models import ScheduledUpdates, TwitterAccount, FacebookAccount, Account
import datetime


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

def schedule(request):
  now = datetime.datetime.now()
  year_list = [now.year, now.year + 1]
  month_list = [x for x in range(1, 13)]
  day_list = [x for x in range(1, 32)]
  hour_list = [x for x in range(0, 24)]
  minute_list = [x for x in range(0, 60)]
  second_list = [x for x in range(0, 60)]
  return render(request, 'schedule.html', {'year_list': year_list, \
      'month_list': month_list, 'day_list': day_list, \
      'hour_list': hour_list, 'minute_list': minute_list, \
      'second_list': second_list})

@login_required
def scheduled_update(request):
  # TODO handle a post/tweet that will be processed at a later date
  request_json = request.POST
  print "into view schedule"
  date_to_post = datetime.datetime(
                    request_json.get('year'), \
                    request_json.get('month'), \
                    request_json.get('day'), \
                    request_json.get('hour'),  \
                    request_json.get('minute'), \
                    request_json.get('second'), \
                    request_json.get('microsecond') \
                  )
  scheduled_update_entry = ScheduledUpdates(user_id=request.user, update=request_json.get('message'), publish_date=date_to_post, publish_site=request_json.get('post_site'))
  scheduled_update_entry.save()
