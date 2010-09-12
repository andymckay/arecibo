import os

from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner

from django.core import mail
from django.core.mail.backends import locmem

from google.appengine.api import mail
from django.core.mail.message import EmailMessage

os.environ['SERVER_SOFTWARE'] = "Development"
settings.DATABASES['default']['SUPPORTS_TRANSACTIONS'] = True

# amongst other things this will suppress those annoying logs
settings.DEBUG = False

def send_email_dummy(sender=None, to=None, subject=None, body=None):
    # app engine doesn't use the backend, so that if you try to write
    # unit tests that check the mail api, they fail, this patches it
    # back in, for the purpose of unit_tests
    return EmailMessage(subject, body, sender, [to,], connection=None).send()

class AreciboRunner(DjangoTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        super(AreciboRunner, self).setup_test_environment(**kwargs)
        mail.send_mail = send_email_dummy