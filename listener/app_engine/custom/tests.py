from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from app.tests import test_data as data
from error.models import Error, Group
from error import signals

from custom.examples import default_public

class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()

    def testNotDefaultAsPublic(self):
        signals.error_created.disconnect(default_public.default_public, dispatch_uid="default_public")
        
        c = Client()
        assert not Error.objects.all().count()
        c.post(reverse("error-post"), data)
        assert Error.objects.all().count() == 1
        assert Error.objects.all()[0].public == False
        
    def testDefaultAsPublic(self):
        signals.error_created.connect(default_public.default_public, dispatch_uid="default_public")
        
        c = Client()
        assert not Error.objects.all().count()
        c.post(reverse("error-post"), data)
        assert Error.objects.all().count() == 1
        assert Error.objects.all()[0].public == True
        
        signals.error_created.disconnect(default_public.default_public, dispatch_uid="default_public")