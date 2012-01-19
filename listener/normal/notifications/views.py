import sys
from datetime import datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template

from notifications.models import Notification
from notifications.email import send_error_email

from app.decorators import arecibo_login_required
from app.paginator import Paginator, get_page
from app.utils import log, render_plain


@arecibo_login_required
def notifications_list(request):
    queryset = Notification.objects.all().order_by("-timestamp")
    paginated = Paginator(queryset, 10)
    page = get_page(request, paginated)
    return direct_to_template(request, "notification_list.html", extra_context={
        "page": page,
        "nav": {"selected": "notifications"}
        })
