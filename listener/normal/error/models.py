from django.core.urlresolvers import reverse
from django.db import models

from datetime import datetime

from error.signals import error_created, group_created
from projects.models import ProjectURL

from app.utils import trunc_string
import os

class Group(models.Model):
    """ A grouping of errors """
    uid = models.CharField(max_length=255, db_index=True)
    timestamp = models.DateTimeField(db_index=True)
    project_url = models.ForeignKey(ProjectURL, null=True, db_index=True)
    count = models.IntegerField(default=0, db_index=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        if self.name:
            return self.name
        elif self.project_url:
            return "%s: %s..." % (self.project_url, self.uid[:10])
        else:
            return unicode(self.uid)

    def sample(self):
        try:
            return Error.objects.filter(group=self).order_by("-timestamp")[0]
        except IndexError:
            return None

    def save(self, *args, **kw):
        created = not getattr(self, "id", None)
        if created:
            self.timestamp = datetime.now()
            group_created.send(sender=self.__class__, instance=self)
        super(Group, self).save(*args, **kw)

class Error(models.Model):
    # time error was received by this server
    timestamp = models.DateTimeField(db_index=True)
    timestamp_date = models.DateField(db_index=True)

    ip = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    user_agent_short = models.CharField(max_length=255)
    user_agent_parsed = models.BooleanField(default=False)
    operating_system = models.CharField(max_length=255)

    priority = models.IntegerField(default=0, db_index=True)
    status = models.CharField(max_length=255, db_index=True)

    raw = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, db_index=True)
    server = models.CharField(max_length=255, db_index=True)
    query = models.CharField(max_length=255)
    protocol = models.CharField(max_length=255)

    uid = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=255, db_index=True)
    msg = models.TextField()
    traceback = models.TextField()

    errors = models.TextField()

    # time error was recorded on the client server
    error_timestamp = models.DateTimeField()
    error_timestamp_date = models.DateTimeField(db_index=True)

    request = models.TextField()
    username = models.CharField(max_length=255, db_index=True)

    group = models.ForeignKey(Group, blank=True, null=True)

    read = models.BooleanField(default=False, db_index=True)

    create_signal_sent = models.BooleanField(default=False)

    public = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-timestamp', '-id']

    def get_absolute_url(self):
        return reverse("error-view", args=[self.id,])

    def has_group(self):
        return self.group

    def get_similar(self, limit=5):
        return (Error.objects.filter(group=self.group)
                             .exclude(pk=self.pk)[:limit])

    def delete(self):
        # TODO: improve this
        if self.group:
            self.group.count = self.group.count - 1
            if self.group.count < 1:
                self.group.delete()
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
        if created:
            self.error_timestamp = datetime.now()
            self.error_timestamp_date = self.error_timestamp.date()
            self.create_signal_sent = True
            super(Error, self).save(*args, **kw)
            error_created.send(sender=self.__class__, instance=self)
        else:
            super(Error, self).save(*args, **kw)
