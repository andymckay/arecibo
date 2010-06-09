import os
from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import connection

from app.tests import test_data as data
from error.models import Error, Group

class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()

    def testBasic(self):
        c = Client()
        assert not Error.all().count()
        res = c.post(reverse("error-post"), data)
        assert Error.all().count() == 1

    def testOverPriority(self):
        c = Client()
        assert not Error.all().count()
        ldata = data.copy()
        ldata["priority"] = 123
        res = c.post(reverse("error-post"), ldata)
        assert Error.all().count() == 1

    def testStringPriority(self):
        c = Client()
        assert not Error.all().count()
        ldata = data.copy()
        ldata["priority"] = "test"
        res = c.post(reverse("error-post"), ldata)
        assert Error.all().count() == 1

    def testNoPriority(self):
        c = Client()
        assert not Error.all().count()
        ldata = data.copy()
        del ldata["priority"]
        res = c.post(reverse("error-post"), ldata)
        assert Error.all().count() == 1

    def testGroup(self):
        c = Client()
        res = c.post(reverse("error-post"), data)
        assert Group.all().count() == 1
        res = c.post(reverse("error-post"), data)
        assert Group.all().count() == 1
        new_data = data.copy()
        new_data["status"] = 402
        res = c.post(reverse("error-post"), new_data)
        assert Group.all().count() == 2

        # and test similar
        assert not Error.all()[2].get_similar()
        assert len(Error.all()[1].get_similar()) == 1
        assert len(Error.all()[1].get_similar()) == 1

    def testBrowser(self):
        c = Client()
        assert not Error.all().count()
        ldata = data.copy()
        ldata["user_agent"] = "Mozilla/5.0 (compatible; Konqueror/3.5; Linux; X11; de) KHTML/3.5.2 (like Gecko) Kubuntu 6.06 Dapper"
        res = c.post(reverse("error-post"), ldata)
        assert Error.all().count() == 1
        assert Error.all()[0].user_agent_short == "Konqueror"
        assert Error.all()[0].user_agent_parsed == True
        assert Error.all()[0].operating_system == "Linux"