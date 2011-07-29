import os
from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import connection

from app import tests
from error.models import Error

def create_error():
    return Error(timestamp=datetime.now(),
                 timestamp_date=datetime.today())


class StatsTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        settings.ANONYMOUS_ACCESS = True
        Error.objects.all().delete()
    
    def testCount(self):
        for x in range(0, 10):
            create_error().save()
    
        for x in range(0, 5):
            err = create_error()
            err.priority = 4
            err.save()

        url = reverse('stats-view', args=['priority'])
        res = self.client.get(url)
        assert 'data.setValue(0, 1, 10);' in res.content
        assert 'data.setValue(0, 2, 5);' in res.content