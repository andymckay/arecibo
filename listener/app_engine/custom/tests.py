from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from app.tests import test_data as data
from error.models import Error, Group

class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()

    def testDefaultAsPublic(self):
        from custom.examples import default_public
        
        c = Client()
        assert not Error.objects.all().count()
        c.post(reverse("error-post"), data)
        assert Error.objects.all().count() == 1
        assert Error.objects.all()[0].public == True