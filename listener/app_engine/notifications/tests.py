import os
from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from error.models import Error
from notifications.models import Notification

from app.tests import test_data

class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()
        for notification in Notification.all(): notification.delete()
        
    def testBasic(self):
        c = Client()
        assert not Error.all().count()        
        res = c.post(reverse("error-post"), test_data)
        assert test_data["priority"] < 5, test_data["priority"]
        assert Error.all().count() == 1
        assert Notification.all().count() == 1

        res = c.post(reverse("error-post"), test_data)
        assert test_data["priority"] < 5, test_data["priority"]
        assert Error.all().count() == 2
        assert Notification.all().count() == 2

    def testNoNotification(self):
        c = Client()
        assert not Error.all().count()        
        data = test_data.copy()
        data["priority"] = 6
        res = c.post(reverse("error-post"), data)
        assert data["priority"] > 5, data["priority"]
        assert Error.all().count() == 1
        assert Notification.all().count() == 0
