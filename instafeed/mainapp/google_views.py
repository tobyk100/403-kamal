from django.http import HttpResponse, HttpResponseRedirect
import json
import google_api
from models import GoogleAccount
from oauth2client.client import OAuth2WebServerFlow

def google_signup(request):
  client_id = google_api.CLIENT_ID
  client_secret = google_api.CLIENT_SECRET
  scope = 'https://www.googleapis.com/auth/userinfo.profile'
  redirect_uri = google_api.REDIRECT_URI + '/google_callback_token'
  flow = OAuth2WebServerFlow(client_id, client_secret, scope, redirect_uri)
  auth_uri = flow.step1_get_authorize_url()
  return HttpResponseRedirect(auth_uri)
