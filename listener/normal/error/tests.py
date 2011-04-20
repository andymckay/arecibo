# -*- coding: UTF8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from app.tests import test_data as data
from app.utils import trunc_string
from error.models import Error, Group

class ErrorTests(TestCase):
    # test the view for writing errors
    
    def testBasic(self):
        c = Client()
        assert not Error.objects.count()
        c.post(reverse("error-post"), data)
        assert Error.objects.count() == 1

    def testOverPriority(self):
        c = Client()
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["priority"] = 123
        c.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1

    def testStringPriority(self):
        c = Client()
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["priority"] = "test"
        c.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1

    def testNoPriority(self):
        c = Client()
        assert not Error.objects.count()
        ldata = data.copy()
        del ldata["priority"]
        c.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1

    def testGroup(self):
        c = Client()
        c.post(reverse("error-post"), data)
        assert Group.objects.count() == 1, "Got %s groups, not 1" % Group.objects.count()
        c.post(reverse("error-post"), data)
        assert Group.objects.count() == 1
        new_data = data.copy()
        new_data["status"] = 402
        c.post(reverse("error-post"), new_data)
        assert Group.objects.count() == 2

        # and test similar
        assert not Error.objects.all()[2].get_similar()
        assert len(Error.objects.all()[1].get_similar()) == 1
        assert len(Error.objects.all()[1].get_similar()) == 1

    def testGroupDelete(self):
        c = Client()
        c.post(reverse("error-post"), data)
        assert Group.objects.count() == 1, "Got %s groups, not 1" % Group.objects.count()
        assert Error.objects.count() == 1
        Error.objects.all()[0].delete()
        assert Group.objects.count() == 0

    def testBrowser(self):
        c = Client()
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["user_agent"] = "Mozilla/5.0 (compatible; Konqueror/3.5; Linux; X11; de) KHTML/3.5.2 (like Gecko) Kubuntu 6.06 Dapper"
        c.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1
        assert Error.objects.all()[0].user_agent_short == "Konqueror"
        assert Error.objects.all()[0].user_agent_parsed == True
        assert Error.objects.all()[0].operating_system == "Linux"

    # http://github.com/andymckay/arecibo/issues#issue/14
    def testUnicodeTraceback(self):
        c = Client()
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["traceback"] = "ɷo̚حٍ"
        c.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1
    
class TagsTests(TestCase):
    def testTrunc(self):
        assert trunc_string("Test123", 5) == "Te..."
        assert trunc_string(None, 5) == ""