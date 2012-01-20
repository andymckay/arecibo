from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from notifications.models import Notification
from app.utils import log, render_plain

class Command(BaseCommand):
    def handle(self, *args, **options):
        notifications_cleanup()

def notifications_cleanup(days=0):
    log("Firing cron: notifications_cleanup")
    expired = datetime.today() - timedelta(days=days)
    queryset = Notification.objects.filter(tried=True, timestamp__lt=expired)
    for notification in queryset:
        notification.delete()

    return render_plain("Cron job completed")

