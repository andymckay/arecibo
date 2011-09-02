# -*- coding: UTF8 -*-
import os
from django.test import TestCase
from django.test.client import Client
from django.core.cache import cache
from django.core.urlresolvers import reverse

from app.tests import test_data as data
from app.utils import trunc_string
from error.models import Error, Group
from error.agent import get

class ErrorTests(TestCase):
    # test the view for writing errors

    def testBasic(self):
        assert not Error.objects.count()
        self.client.post(reverse("error-post"), data)
        assert Error.objects.count() == 1

    def testOverPriority(self):
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["priority"] = 123
        self.client.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1

    def testStringPriority(self):
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["priority"] = "test"
        self.client.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1

    def testNoPriority(self):
        assert not Error.objects.count()
        ldata = data.copy()
        del ldata["priority"]
        self.client.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1

    def testGroup(self):
        self.client.post(reverse("error-post"), data)
        assert Group.objects.count() == 1, "Got %s groups, not 1" % Group.objects.count()
        self.client.post(reverse("error-post"), data)
        assert Group.objects.count() == 1
        new_data = data.copy()
        new_data["status"] = 402
        self.client.post(reverse("error-post"), new_data)
        assert Group.objects.count() == 2

        # and test similar
        assert not Error.objects.order_by('pk')[2].get_similar()
        assert len(Error.objects.order_by('pk')[1].get_similar()) == 1
        assert len(Error.objects.order_by('pk')[0].get_similar()) == 1

    def testGroupDelete(self):
        self.client.post(reverse("error-post"), data)
        assert Group.objects.count() == 1, "Got %s groups, not 1" % Group.objects.count()
        assert Error.objects.count() == 1
        Error.objects.all()[0].delete()
        assert Group.objects.count() == 0

    def testBrowser(self):
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["user_agent"] = "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.8.0.5) Gecko/20060731 Ubuntu/dapper-security Firefox/1.5.0.5"
        self.client.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1
        assert Error.objects.all()[0].user_agent_short == "Firefox"
        assert Error.objects.all()[0].user_agent_parsed == True
        assert Error.objects.all()[0].operating_system == "Linux"

    # http://github.com/andymckay/arecibo/issues#issue/14
    def testUnicodeTraceback(self):
        assert not Error.objects.count()
        ldata = data.copy()
        ldata["traceback"] = "ɷo̚حٍ"
        self.client.post(reverse("error-post"), ldata)
        assert Error.objects.count() == 1

    def testCount(self):
        ldata = data.copy()
        ldata["count"] = 5
        self.client.post(reverse("error-post"), ldata)
        assert Group.objects.count() == 1
        assert Group.objects.all()[0].count == 5

    def testCountUpdate(self):
        ldata = data.copy()
        self.client.post(reverse("error-post"), ldata)
        assert Group.objects.all()[0].count == 1

        ldata["count"] = 5
        self.client.post(reverse("error-post"), ldata)
        assert Group.objects.all()[0].count == 6

    def testGroupTimestampUpdates(self):
        self.client.post(reverse("error-post"), data)
        group = Group.objects.all()[0]
        old = group.timestamp
        self.client.post(reverse("error-post"), data)
        group = Group.objects.all()[0]
        assert group.timestamp != old


class TagsTests(TestCase):
    def testTrunc(self):
        assert trunc_string("Test123", 5) == "Te..."
        assert trunc_string(None, 5) == ""

class AgentTests(TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), 'fixtures/browscap.ini')
        raw = open(path).read()
        key = "browser-capabilities-raw"
        cache.set(key, raw)

    def testAgent(self):
        bc = get()
        for agent in [
            "Mozilla/5.0 (compatible; Konqueror/3.5; Linux; X11; de) KHTML/3.5.2 (like Gecko) Kubuntu 6.06 Dapper",
            "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.8.0.5) Gecko/20060731 Ubuntu/dapper-security Firefox/1.5.0.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20060216 Debian/1.7.12-1.1ubuntu2",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.5) Gecko/20060731 Ubuntu/dapper-security Epiphany/2.14 Firefox/1.5.0.5",
            "Opera/9.00 (X11; Linux i686; U; en)",
            "Wget/1.10.2",
            "Mozilla/5.0 (X11; U; Linux i386) Gecko/20063102 Galeon/1.3test",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_4; en-us) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)" # Tested under Wine
            """Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US;  \r
    rv:1.9.0.5) Gecko/2008120121 Firefox/3.0.5,gzip(gfe)""",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.5) Gecko/2008120121 Firefox/3.0.5,gzip(gfe)",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1,gzip(gfe)"
          ]:
            b = bc(agent)
            assert b.name()
