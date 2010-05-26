import os
from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.files import File
from django.conf import settings
from django.db import connection

from error.models import Error

settings.DATABASES['default']['SUPPORTS_TRANSACTIONS'] = True

data = {
    "account": settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER,
    "priority": 4,
    "user_agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X...",
    "url": "http://badapp.org/-\ufffdwe-cant-lose",
    "uid": "123124123123",
    "ip": "127.0.0.1",    
    "type": "Test from python",
    "status": "403",
    "server": "Test Script", 
    "request": """This is the bit that goes in the request""",
    "username": "Jimbob",
    "msg": """
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut 
labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit 
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in 
culpa qui officia deserunt mollit anim id est laborum
""",
    "traceback": """Traceback (most recent call last",:
File "<stdin>", line 1, in <module>
ZeroDivisionError: integer division or modulo by zero  df
""",}

class ErrorTests(TestCase):
    # test the view for writing errors
    def setUp(self):
        for error in Error.all(): error.delete()
        
    def testBasic(self):
        c = Client()
        assert not Error.all().count()        
        res = c.post(reverse("error-post"), data)
        assert Error.all().count() == 1

    def testOverPriority(self):
        c = Client()
        assert not Error.all().count()        
        ldata = data.copy()
        ldata["priority"] = 123
        res = c.post(reverse("error-post"), ldata)
        assert Error.all().count() == 1
            
    def testStringPriority(self):
        c = Client()
        assert not Error.all().count()        
        ldata = data.copy()
        ldata["priority"] = "test"
        res = c.post(reverse("error-post"), ldata)
        assert Error.all().count() == 1
                            
    def testNoPriority(self):
        c = Client()
        assert not Error.all().count()        
        ldata = data.copy()
        del ldata["priority"]
        res = c.post(reverse("error-post"), ldata)
        assert Error.all().count() == 1    