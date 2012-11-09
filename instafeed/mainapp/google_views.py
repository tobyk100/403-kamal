from django.http import HttpResponse, HttpResponseRedirect
import json, httplib2
import google_api
from models import GoogleAccount, CredentialsModel
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage
from django.contrib.auth.decorators import login_required
from apiclient.discovery import build
from django.shortcuts import render_to_response


client_id = google_api.CLIENT_ID
client_secret = google_api.CLIENT_SECRET
scope = 'https://www.googleapis.com/auth/userinfo.profile'
redirect_uri = google_api.REDIRECT_URI + '/google_callback_token'
FLOW = OAuth2WebServerFlow(client_id, client_secret, scope, redirect_uri)

def google_signup(request):
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    auth_uri = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(auth_uri)
  else:
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build("plus", "v1", http=http)
    activities = service.activities()
    activitylist = activities.list(collection='public', userId='me').execute()
    render_to_response('/', {"activity_list": activitylist})

def google_callback_token(request):
  credential = FLOW.step2_exchange(request.REQUEST)
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
  storage.put(credential)
  return HttpResponseRedirect("/")
