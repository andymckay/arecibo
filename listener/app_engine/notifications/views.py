import sys
from datetime import datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.views.generic.simple import direct_to_template

from notifications.models import Notification
from notifications.email import send_error_email

from app.paginator import Paginator, get_page
from app.utils import log, render_plain

@user_passes_test(lambda u: u.is_staff)
def notifications_list(request):
    queryset = Notification.all().order("-timestamp")
    # this number doesn't need to be high and its quite an expensive
    # page to generate
    paginated = Paginator(queryset, 10)
    page = get_page(request, paginated)
    return direct_to_template(request, "notification_list.html", extra_context={
        "page": page,
        "nav": {"selected": "notifications"}
        })


def notifications_cleanup(request):
    log("Firing cron: notifications_cleanup")
    expired = datetime.today() - timedelta(days=7)
    queryset = Notification.all().filter("tried = ", True).filter("timestamp < ", expired)
    for notification in queryset:
        notification.delete()

    return render_plain("Cron job completed")

class Holder:
    def __init__(self):
        self.user = None
        self.objs = []
        self.notifs = []

def notifications_send(request):
    log("Firing cron: notifications_send")
    notifications = Notification.all().filter("tried = ", False)

    # batch up the notifications for the user
    holders = {}
    for notif in notifications:
        for user in notif.user_list():
            key = str(user.key())
            if key not in holders:
                holder = Holder()
                holder.user = user
                holders[key] = holder

            holders[key].objs.append(notif.error)
            holders[key].notifs.append(notif)

    for user_id, holder in holders.items():
        try:
            send_error_email(holder)
            for notification in holder.notifs:
                notification.tried = True
                notification.completed = True
                notification.save()
        except:
            info = sys.exc_info()
            data = "%s, %s" % (info[0], info[1])
            for notification in holder.notifs:
                notification.tried = True
                notification.completed = True
                notification.error_msg = data
                notification.save()

    return render_plain("Cron job completed")