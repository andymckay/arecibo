from django.core.urlresolvers import reverse
from django.db import models

from datetime import datetime

from error.signals import group_created
from projects.models import ProjectURL

from app.utils import trunc_string
from app.base import Base
import os

class Group(models.Model):
    """ A grouping of errors """
    uid = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    project_url = models.ForeignKey(ProjectURL, null=True)
    count = models.IntegerField(default=0)

    def sample(self):
        try:
            return Error.all().filter("group = ", self).order("-timestamp")[0]
        except IndexError:
            return None

    def save(self, *args, **kw):
        created = not getattr(self, "id", None)
        if created:
            self.timestamp = datetime.now()
        self.put()
        if created:
            group_created.send(sender=self.__class__, instance=self)

class Error(models.Model):
    # time error was received by this server
    timestamp = models.DateTimeField()
    timestamp_date = models.DateField()

    ip = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    user_agent_short = models.CharField(max_length=255)
    user_agent_parsed = models.BooleanField(default=False)
    operating_system = models.CharField(max_length=255)

    priority = models.IntegerField(default=0)
    status = models.CharField(max_length=255)

    raw = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    server = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    protocol = models.CharField(max_length=255)

    uid = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    msg = models.TextField()
    traceback = models.TextField()

    errors = models.TextField()

    # time error was recorded on the client server
    error_timestamp = models.DateTimeField()
    request = models.TextField()
    username = models.CharField(max_length=255)

    group = models.ForeignKey(Group)

    read = models.BooleanField(default=False)

    create_signal_sent = models.BooleanField(default=False)

    public = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("error-view", args=[self.id,])

    def has_group(self):
        try:
            return self.group
        except db.Error:
            return []

    def get_similar(self, limit=5):
        try:
            return Error.all().filter("group = ", self.group).filter("__key__ !=", self.key())[:limit]
        except db.Error:
            return []

    def delete(self):
        try:
            if self.group:
                self.group.count = self.group.count - 1
                if self.group.count < 1:
                    self.group.delete()
        except db.Error:
            pass
        super(Error, self).delete()

    @property
    def title(self):
        """ Try to give a nice title to describe the error """
        strng = ""
        if self.type:
            strng = self.type
            if self.server:
                if self.status:
                    strng = "%s" % (strng)
                if not strng:
                    strng = "Error"
                strng = "%s on %s" % (strng, self.server)
        elif self.status:
            strng = self.status
            if self.server:
                strng = "%s on server %s" % (strng, self.server)
        elif self.raw:
            strng = self.raw
        else:
            strng = self.error_timestamp.isoformat()
        if self.uid:
            strng = "%s" % (strng)
        return strng

    @property
    def description(self):
        return self.msg or ""

    def save(self, *args, **kw):
        created = not getattr(self, "id", None)
        self.put()
        if created and not "dont_send_signals" in kw:
            if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
                # send the signal, otherwise we have to clicking buttons
                # to process the queue
                from error.views import send_signal
                send_signal(None, self.id)
            else:
                # enqueue the send notification
                # if development
                taskqueue.add(url=reverse("error-created", args=[self.id,]))

#from notifications import registry
#registry.register(Error, "Error")