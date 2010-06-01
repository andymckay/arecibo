from datetime import datetime

from appengine_django.models import BaseModel
from appengine_django.auth.models import User

from google.appengine.ext import db

from error.signals import error_created
from notifications.signals import notification_created
from users.utils import approved_users
from app.utils import log

class Notification(BaseModel):
    # to do, fix this
    from error.models import Error
    
    user = db.ListProperty(str)
    error = db.ReferenceProperty(Error)
    
    tried = db.BooleanProperty(default=False)
    completed = db.BooleanProperty(default=False)
    error_msg = db.TextProperty()
    timestamp = db.DateTimeProperty()
    
    def save(self):
        created = not hasattr(self, "id")
        if created:
            self.timestamp = datetime.now()
        self.put()
        if created:
            notification_created.send(sender=self.__class__, instance=self)

    def user_list(self):
        return [ User.get(key) for key in self.user ]