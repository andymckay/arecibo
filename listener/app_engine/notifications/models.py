from datetime import datetime
from django.db import models

from appengine_django.models import BaseModel
from appengine_django.auth.models import User

from google.appengine.ext import db

from error.models import Error
from notifications.signals import notification_created

class Notification(BaseModel):
    user = db.ListProperty(str)
    error = db.ReferenceProperty(Error)
    
    tried = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    error_msg = models.TextField()
    timestamp = db.DateTimeProperty()
    
    def save(self):
        created = not hasattr(self, "id")
        if created:
            self.timestamp = datetime.now()
        self.put()
        if created:
            notification_created.send(sender=self.__class__, instance=self)
    
from notifications import creating