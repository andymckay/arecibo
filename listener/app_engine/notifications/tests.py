from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from error.models import Error
from issues.models import Issue
from notifications.models import Notification
from appengine_django.auth.models import User as AppUser
from google.appengine.api.users import User
from profiles.utils import get_profile

from app.tests import test_data
from django.core import mail

def create_user():
    return AppUser(user=User(email="test@foo.com"),
                    username="test",
                    email="test@foo.com",
                    is_staff=True).save()


class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()
        for notification in Notification.all(): notification.delete()
        for user in AppUser.all(): user.delete()
        for issue in Issue.all(): issue.delete()

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

    def testProfile(self):
        user = create_user()        
        
        c = Client()
        data = test_data.copy()
        data["priority"] = 6
        c.post(reverse("error-post"), data)
        
        assert Notification.all().count() == 0, Notification.all().count()
    
        data["priority"] = 5
        c.post(reverse("error-post"), data)
        
        assert Notification.all().count() == 1
        
        profile = get_profile(user)
        profile.notification = 8

        data["priority"] = 5
        c.post(reverse("error-post"), data)
        
        assert Notification.all().count() == 2
        
        data["priority"] = 8
        c.post(reverse("error-post"), data)
        
        assert Notification.all().count() == 2

        data["priority"] = 9
        c.post(reverse("error-post"), data)
        
        assert Notification.all().count() == 2

    def testNotificationNoUsers(self):
        c = Client()
        c.post(reverse("error-post"), test_data)
        assert Notification.all().count() == 0
    
    def testIssueAndErrorNotification(self):
        user = create_user()
        
        issue = Issue()
        issue.description = "This is a test"
        issue.save()
        
        assert Issue.all().count() == 1

        c = Client()
        c.post(reverse("error-post"), test_data)

        #assert Notification.all().count() == 2
        # this would be 2 when issues are turned on
        assert Notification.all().count() == 1
        
        c = Client()
        res = c.get(reverse("notification-send"))        
        self.assertEquals(len(mail.outbox), 1)
        
        # this is to check that at the moment issue notifications don't get sent
    
    def testIssueNotification(self):
        user = create_user()
    
        issue = Issue()
        issue.description = "This is a test"
        issue.save()
        
        assert Issue.all().count() == 1
        #assert Notification.all().count() == 1
        #assert Notification.all()[0].type == "Issue"
    
    def testCron(self):
        user = create_user()
        
        self.testBasic()
        # now test our sending actually works
        c = Client()
        res = c.get(reverse("notification-send"))        
        self.assertEquals(len(mail.outbox), 1)