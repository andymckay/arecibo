from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from error.models import Error, Group
from projects.models import Project, ProjectURL

from app.tests import test_data
from app.utils import _pdb

class ProjectTests(TestCase):
    # test the signals for project
    def setUp(self):
        for error in Error.all(): error.delete()
        for group in Group.all(): group.delete()
        for project in Project.all(): project.delete()
    
    def _addError(self):
        c = Client()
        assert not Error.all().count()
        c.post(reverse("error-post"), test_data)
        assert test_data["priority"] < 5, test_data["priority"]
        assert Error.all().count() == 1

    def testAddProject(self):
        project = Project(name="test")
        project.save()
        
        project_url = ProjectURL()
        project_url.url = "badapp.org"
        project_url.stage = "dev"
        project_url.project = project
        project_url.save()
        
        self._addError()
        
        assert Group.all().count() == 1
        assert Group.all()[0].project_url == project_url