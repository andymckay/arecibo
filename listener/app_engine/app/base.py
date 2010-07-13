from appengine_django.models import BaseModel
from google.appengine.ext import db

class Base(BaseModel):
    @property
    def id(self):
        try:
            return str(self.key())
        except db.NotSavedError:
            pass
