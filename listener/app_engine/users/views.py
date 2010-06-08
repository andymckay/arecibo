import sys
from datetime import datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from appengine_django.auth.models import User

from google.appengine.ext import db

from users.utils import approved_users

from app.paginator import Paginator, get_page
from app.utils import log

@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    queryset = User.all()
    # this number doesn't need to be high and its quite an expensive
    # page to generate
    paginated = Paginator(queryset, 10)
    page = get_page(request, paginated)
    return direct_to_template(request, "user_list.html", extra_context={
        "page": page, 
        "nav": {"selected": "setup"}
        })

@user_passes_test(lambda u: u.is_staff)
def user_change(request, pk):
    user = User.get(pk)
    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect(reverse("user-list"))

