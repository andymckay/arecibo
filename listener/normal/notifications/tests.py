from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from error.models import Error
from notifications.models import Notification

from app.tests import test_data
from django.core import mail

class ErrorTests(TestCase):
    # test the view for writing errors
    def testBasic(self):
        c = Client()
        assert not Error.objects.all().count()
        c.post(reverse("error-post"), test_data)
        assert test_data["priority"] < 5, test_data["priority"]
        assert Error.objects.all().count() == 1, Error.objects.all().count()

        c.post(reverse("error-post"), test_data)
        assert test_data["priority"] < 5, test_data["priority"]
        assert Error.objects.all().count() == 2

    def testNoNotification(self):
        c = Client()
        assert not Error.objects.all().count()
        data = test_data.copy()
        data["priority"] = 6
        c.post(reverse("error-post"), data)
        assert data["priority"] > 5, data["priority"]
        assert Error.objects.all().count() == 1
        assert Notification.objects.all().count() == 0

    def testNotificationNoUsers(self):
        c = Client()
        c.post(reverse("error-post"), test_data)
        assert Notification.objects.all().count() == 0

    def testCron(self):
        User(email="test@foo.com",
             username="test",
             is_staff=True).save()
        self.testBasic()
        # now test our sending actually works
        c = Client()
        res = c.get(reverse("notification-send"))
        self.assertEquals(len(mail.outbox), 1)
