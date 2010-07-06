from django.utils import simplejson

from datetime import datetime

from google.appengine.ext import db

from appengine_django.models import BaseModel
from stats.signals import stats_completed

class Stats(BaseModel):
    """ A series of stats for a date """
    date = db.DateProperty()
    timestamp = db.DateTimeProperty()
    stats = db.TextProperty()
    completed = db.BooleanProperty(default=False)

    @property
    def id(self):
        return str(self.key())

    def save(self, *args, **kw):
        created = not hasattr(self, "id")
        if created:
            self.timestamp = datetime.now()

        if not self.completed and self.complete():
            self.completed = True
            self.put()
            stats_completed.send(sender=self.__class__, instance=self)
        else:
            self.put()

    def get_stats(self):
        if self.stats:
            return simplejson.loads(self.stats)
        return simplejson.loads("{}")

    def set_stats(self, data):
        self.stats = simplejson.dumps(data)

    def complete(self):
        values = self.get_stats().values()
        if not values:
            return False
        return not None in values
