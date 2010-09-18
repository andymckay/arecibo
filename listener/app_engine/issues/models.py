from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from datetime import datetime

from google.appengine.api.labs import taskqueue
from google.appengine.ext import db

from appengine_django.auth.models import User

from userstorage.utils import get_user

from app.base import Base
from app.utils import break_url, trunc_string
from projects.models import Project, ProjectURL
from error.models import Group
from issues import signals

class Issue(Base):
    # time error was received by this server
    timestamp = db.DateTimeProperty()

    title = db.StringProperty(required=False)
    description = db.TextProperty(required=False)

    priority = db.IntegerProperty()

    raw = db.StringProperty()
    domain = db.StringProperty()
    query = db.StringProperty()
    protocol = db.StringProperty()

    project = db.ReferenceProperty(Project, required=False)
    creator = db.ReferenceProperty(User, required=False, collection_name="creator")
    assigned = db.ReferenceProperty(User, required=False, collection_name="assignee")

    status = db.StringProperty()

    number = db.IntegerProperty()

    def get_absolute_url(self):
        return reverse("issues-view", args=[self.number,])

    def get_log_set(self):
        """ We need to provide a way to order the logs """
        return self.log_set.order("-timestamp")

    def get_comment_set(self):
        """ We need to provide a way to order the comments """
        return self.comment_set.order("-timestamp")

    def add_log(self, text):
        """ Adds in a log on the issue for the current user """
        log = Log(creator=get_user(), timestamp=datetime.now(), text=text, issue=self)
        log.save()
        return log

    def add_group(self, group):
        """ Adds in an issue group """
        issue_group = IssueGroup(issue=self, group=group)
        issue_group.save()
        return issue_group

    def __str__(self):
        return self.title

    def save(self, *args, **kw):
        if self.raw:
            for k, v in break_url(self.raw).items():
                setattr(self, k, v)

        if not self.title:
            self.title = trunc_string(self.description, 50)

        created = not getattr(self, "id", None)
        old = None
        if created:
            # there's a possible race condition here
            try:
                self.number = Issue.all().order("-number")[0].number + 1
            except IndexError:
                self.number = 1
            self.timestamp = datetime.now()
        else:
            old = Issue.get(self.id)

        self.put()
        if created:
            signals.issue_created.send(sender=self.__class__, instance=self)
        else:
            for key in ["status", "assigned", "priority"]:
                new_value = getattr(self, key)
                old_value = getattr(old, key)
                if new_value !=old_value:
                    signal = getattr(signals, "issue_%s_changed" % key)
                    signal.send(sender=self.__class__, instance=self, old=old_value, new=new_value)

            signals.issue_changed.send(sender=self.__class__, instance=self, old=old)

class Comment(Base):
    timestamp = db.DateTimeProperty()
    issue = db.ReferenceProperty(Issue)
    text = db.TextProperty()

    creator = db.ReferenceProperty(User)

    def save(self, *args, **kw):
        created = not getattr(self, "id", None)
        if created:
            self.timestamp = datetime.now()

        self.put()
        if created:
            signals.comment_created.send(sender=self.__class__, instance=self)

class IssueGroup(Base):
    issue = db.ReferenceProperty(Issue)
    group = db.ReferenceProperty(Group)

class IssueProjectURL(Base):
    issue = db.ReferenceProperty(Issue)
    project_url = db.ReferenceProperty(ProjectURL)
    status = db.StringProperty(required=False)

    def get_status_image(self):
        return {
            "not_fixed": "not-fixed",
            "fixed": "fixed"
        }.get(self.status, "")

    def get_status_display(self):
        from issues.forms import issue_project_url_statuses
        return dict(issue_project_url_statuses).get(self.status)

    def __str__(self):
        return str(self.project_url)

class Log(Base):
    timestamp = db.DateTimeProperty()

    issue = db.ReferenceProperty(Issue)
    text = db.TextProperty()

    creator = db.ReferenceProperty(User)

from notifications import registry
registry.register(Issue, "Issue")