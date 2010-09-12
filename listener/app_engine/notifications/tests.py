from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from error.models import Error
from notifications.models import Notification
from appengine_django.auth.models import User as AppUser
from google.appengine.api.users  import User

from app.tests import test_data
from django.core import mail

class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()
        for notification in Notification.all(): notification.delete()
        for user in AppUser.all(): user.delete()

    def testBasic(self):
        c = Client()
        assert not Error.all().count()
        c.post(reverse("error-post"), test_data)
        assert test_data["priority"] < 5, test_data["priority"]
        assert Error.all().count() == 1

        c.post(reverse("error-post"), test_data)
        assert test_data["priority"] < 5, test_data["priority"]
        assert Error.all().count() == 2

    def testNoNotification(self):
        c = Client()
        assert not Error.all().count()
        data = test_data.copy()
        data["priority"] = 6
        c.post(reverse("error-post"), data)
        assert data["priority"] > 5, data["priority"]
        assert Error.all().count() == 1
        assert Notification.all().count() == 0

    def testNotificationNoUsers(self):
        c = Client()
        c.post(reverse("error-post"), test_data)
        assert Notification.all().count() == 0
                
    def testCron(self):
        AppUser(user=User(email="test@foo.com"),
                username="test",
                email="test@foo.com",
                is_staff=True).save()
        self.testBasic()
        # now test our sending actually works
        c = Client()
        res = c.get(reverse("notification-send"))        
        self.assertEquals(len(mail.outbox), 1)