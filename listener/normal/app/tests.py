# test data
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

try:
    account = settings.ARECIBO_PUBLIC_ACCOUNT_NUMBER
except ImportError:
    account = "1231241243"
        
test_data = {
    "account": account,
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

class TestAppNotAnon(TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        settings.ANONYMOUS_ACCESS = False
        self.url = reverse('setup')

    def test_auth(self):
        assert self.client.login(username='admin', password='password')
        
    def test_decorator(self):
        res = self.client.get(self.url)
        assert res.status_code == 302

    def test_decorator_logged_in(self):
        assert self.client.login(username='admin', password='password')
        res = self.client.get(self.url)
        assert res.status_code == 200

class TestAppAnon(TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        settings.ANONYMOUS_ACCESS = True
        self.url = reverse('setup')

    def test_decorator_anon(self):
        res = self.client.get(self.url)
        assert res.status_code == 200

    def test_decorator_anon_logged_in(self):
        assert self.client.login(username='admin', password='password')
        res = self.client.get(self.url)
        assert res.status_code == 200
