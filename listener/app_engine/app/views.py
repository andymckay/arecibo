import os
from urlparse import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_control

from google.appengine.api import users

#: static_resource cache decorator will be used for things which can safely
# be cached to improve client HTTP performance
static_resource = cache_control(public=True, max_age=86400)

def index(request):
    if request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect(reverse("error-list"))
    return direct_to_template(request, "index.html")

@user_passes_test(lambda u: u.is_staff)
def setup(request):
    return direct_to_template(request, "setup.html", extra_context={
        "nav": {"selected": "setup"},
        "app_id": os.environ.get("APPLICATION_ID"),
        })

@static_resource
@vary_on_headers("Accept-Encoding")
def javascript_client(request):
    return direct_to_template(request, "error.js",
        extra_context = {
            "domain": urlparse(settings.SITE_URL)[1]
        },
        mimetype = "text/javascript",
    )

def logout(request):
    return HttpResponseRedirect(users.create_logout_url("/"))

def login(request):
    return HttpResponseRedirect(users.create_login_url("/"))