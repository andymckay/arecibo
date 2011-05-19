from datetime import datetime

from app.base import Base
from google.appengine.ext import db
from appengine_django.auth.models import User

class Profile(Base):
    user = db.ReferenceProperty(User)
    notification = db.IntegerProperty()

    def __str__(self):
        return str(self.user)
