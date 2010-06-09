import os
from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import connection

from app import tests
from error.models import Error, Group
from stats.utils import count

class StatsTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()
    
    def testCount(self):
        for x in range(0, 1110):
            Error().save(dont_send_signals=True)
        assert count() == 1110
        for x in range(0, 5):
            err = Error(dont_send_signals=True)
            err.priority = 4
            err.save()
        assert count(["priority = ", 4]) == 5
        assert count(["priority = ", None]) == 1110
        assert count() == 1115        