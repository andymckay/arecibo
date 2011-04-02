from datetime import datetime
from django.db import models

from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ManyToManyField(User)

    tried = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    error_msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    type = models.CharField(max_length=255)
    type_key = models.CharField(max_length=255)

    def notifier(self):
        """Returns the object that you'd like to be notified about."""
        if self.type and self.type_key:
            return get()[self.type].get(self.type_key)        

#    def save(self):
#        created = not hasattr(self, "id")
#        self.put()
#        if created:
#            notification_created.send(sender=self.__class__, instance=self)

