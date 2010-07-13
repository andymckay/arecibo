from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from issues.models import Issue, Log, Comment, IssueGroup
from error.models import Group, Error
from projects.models import Project, ProjectURL
from google.appengine.ext import db

from issues import listeners
from error import listeners

from app.utils import break_url
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

    def testIssueGroup(self):
        self._setup()

        issue = Issue()
        issue.description = "This is a test"
        issue.save()

        group = Group.all()[0]
        issue.add_group(group)

        assert group == issue.issuegroup_set[0].group
        assert issue.issuegroup_set.count() == 1

        assert issue == IssueGroup.all().filter("issue = ", issue)[0].issue

    def testIssueURL(self):
        self._setup()

        issue = Issue()
        issue.project = self.project
        issue.description = "This is a test"
        issue.save()

        assert issue.issueprojecturl_set.count() == 2
        assert issue.issueprojecturl_set[0].status == "not_fixed"
