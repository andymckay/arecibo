from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from issues.models import Issue, Log, Comment, IssueGroup
from error.models import Group, Error
from projects.models import Project, ProjectURL
from google.appengine.ext import db

from issues import listeners
from issues import signals
from issues.views import issue_by_number
from error import listeners

from app.utils import break_url, safe_int
from app.utils import _pdb

class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for issue in Issue.all(): issue.delete()
        for log in Log.all(): log.delete()
        for comment in Comment.all(): comment.delete()
        for group in Group.all(): group.delete()
        for error in Error.all(): error.delete()
        for project in Project.all(): project.delete()

    def testLogAdded(self):
        issue = Issue()
        issue.description = "This is a test"
        issue.save()

        assert issue.log_set[0]

    def _setup(self):
        self.project = Project(name="testing")
        self.project.save()

        self.url = ProjectURL(url="http://test.areciboapp.com")
        self.url.project = self.project
        self.url.save()

        self.url = ProjectURL(url="http://www.areciboapp.com")
        self.url.project = self.project
        self.url.save()

        self.error = Error()
        for k, v in break_url("http://test.areciboapp.com/an/other").items():
            setattr(self.error, k, v)
        self.error.save()

    def _issue(self):
        self.issue = Issue()
        self.issue.description = "This is a test"
        self.issue.save()

    def testIssueGroup(self):
        self._setup()

        self._issue()

        group = Group.all()[0]
        self.issue.add_group(group)

        assert group == self.issue.issuegroup_set[0].group
        assert self.issue.issuegroup_set.count() == 1

        assert self.issue == IssueGroup.all().filter("issue = ", self.issue)[0].issue

    def testIssueURL(self):
        self._setup()

        self.issue = Issue()
        self.issue.description = "This is a test"
        self.issue.project = self.project
        self.issue.save()

        assert self.issue.issueprojecturl_set.count() == 2
        assert self.issue.issueprojecturl_set[0].status == "not_fixed"

    def testIssueURLFlexibility(self):
        self._setup()

        self._issue()
        assert self.issue == issue_by_number(self.issue.number)
        assert self.issue == issue_by_number(self.issue.id)

    def testIssueChanged(self):
        self.signal_fired = False
        def signal_fired(instance, old, **kw):
            self.signal_fired = True
        signals.issue_changed.connect(signal_fired, dispatch_uid="issue_changed")
        self._issue()
        self.issue.status = "rejected"
        self.issue.save()
        assert self.signal_fired

    def testIssuePriorityChanged(self):
        self.signal_fired = False
        def signal_fired(instance, old, new, **kw):
            self.signal_fired = True
            assert old in (None, 1)
            assert new in (1, 2)

        signals.issue_priority_changed.connect(signal_fired, dispatch_uid="issue_priority_changed")

        self._issue()
        self.issue.priority = 1
        self.issue.save()
        assert self.signal_fired

        self.signal_fired = False
        self.issue.priority = 2
        self.issue.save()
        assert self.signal_fired

    def testIssueStatusChanged(self):
        self.signal_fired = False
        def signal_fired(instance, old, new, **kw):
            self.signal_fired = True
            assert not old
            assert new == "rejected"

        signals.issue_status_changed.connect(signal_fired, dispatch_uid="issue_status_changed")

        self._issue()
        self.issue.status = "rejected"
        self.issue.save()
        assert self.signal_fired

        self.signal_fired = False
        self.issue.priority = 1
        self.issue.save()
        assert not self.signal_fired
