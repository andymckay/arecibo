from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from google.appengine.api import users

def index(request):
    return direct_to_template(request, "index.html")

def logout(request):
    return HttpResponseRedirect(users.create_logout_url("/"))

def login(request):
    return HttpResponseRedirect(users.create_login_url("/"))