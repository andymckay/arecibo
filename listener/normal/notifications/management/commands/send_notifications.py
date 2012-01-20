import sys

from django.core.management.base import BaseCommand

from notifications.email import send_error_email
from notifications.models import Notification
from app.utils import log, render_plain


class Holder:
    def __init__(self):
        self.user = None
        self.objs = []
        self.notifs = []


class Command(BaseCommand):
    def handle(self, *args, **options):
        notifications_send()


def notifications_send():
    log("Firing cron: notifications_send")
    notifications = Notification.objects.filter(tried=False)

    # batch up the notifications for the user
    holders = {}
    for notif in notifications:
        for user in notif.user.all():
            key = user.pk
            if key not in holders:
                holder = Holder()
                holder.user = user
                holders[key] = holder

            holders[key].objs.append(notif.notifier)
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
