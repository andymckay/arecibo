from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from google.appengine.ext import db

from notifications.models import Notification

from app.paginator import Paginator, get_page

@user_passes_test(lambda u: u.is_staff)
def notifications_list(request):
    queryset = Notification.all().order("-timestamp")
    paginated = Paginator(queryset, 50)
    page = get_page(request, paginated)
    return direct_to_template(request, "notification_list.html", extra_context={
        "page": page, 
        "nav": {"selected": "notifications"}
        })