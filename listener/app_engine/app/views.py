from urlparse import urlparse

from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.conf import settings

from google.appengine.api import users

def index(request):
    return direct_to_template(request, "index.html")

def javascript_client(request):
    return direct_to_template(request, "error.js", extra_context={"domain":urlparse(settings.SITE_URL)[1]})

def logout(request):
    return HttpResponseRedirect(users.create_logout_url("/"))

def login(request):
    return HttpResponseRedirect(users.create_login_url("/"))