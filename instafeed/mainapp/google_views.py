from django.http import HttpResponse
import json, os

def google_signin(request):
  response = {}
  response['message'] = os.environ['SERVER_SOFTWARE']
  return HttpResponse(json.dumps(response), mimetype="application/json")
