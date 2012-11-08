from django.http import HttpResponse, HttpResponseRedirect
import json
import google_api

def google_signin(request):
  response = {}
  token = request.session.get('google_token')
  if (token is None) or (not is_valid(token)):
    token = google_request_token(request)

  return HttpResponse(json.dumps(response))

def google_request_token(request):
  user = request.user
  account = GoogleAccount.get_account(user)
  refresh_token = _request_refresh_token(request) if not account else \
                  account.refresh_token

def google_get_posts(request):
  pass


def google_request_code(request):
  url = google_api.request_code()
  return HttpResponseRedirect(url)

def _request_refresh_token(request):
  request_post = google_api.request_token(request.code)
  url = google_api.request_token_url()
  redirect = HttpResponseRedirect(url)
  redirect.POST.update(request_post)

  return redirect

# returns a json object with the following fields:
#   authorized - A boolean representing whether the user gave us access
def google_callback_code(request):
  response = {}
  response['authorized'] = (request.GET.get('error') != 'access_denied')
  if response['authorized']:
    response['code'] = request.GET.get('code')

  return HttpResponse(json.dumps(response))

def google_callback_token(request):
  pass
