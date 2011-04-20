from datetime import datetime
from django.db import models

from django.contrib.auth.models import User

from error.models import Error
from notifications.signals import notification_created


class Notification(models.Model):
    user = models.ManyToManyField(User)

    tried = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    error_msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    notifier = models.ForeignKey(Error, blank=True, null=True)

    def save(self, *args, **kw):
        created = not getattr(self, "id", None)
        super(Notification, self).save(*args, **kw)
        if created:
            notification_created.send(sender=self.__class__, instance=self)

