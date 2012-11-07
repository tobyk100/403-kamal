from django.shortcuts import redirect
from django.http import HttpResponse
import json, os

def google_signin(request):
  params = {}
  params['response_type'] = 'code'
  params['client_id'] = '138535205339.apps.googleusercontent.com'
  params['redirect_id'] = 'http://dry-peak-6840.herokuapp.com/google_callback'
  params['scope'] = 'https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&'
  return redirect('http://accounts.google.com/o/oauth2/auth', params)
