import os

from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner

from django.core import mail
from django.core.mail.backends import locmem

from django.core.mail.message import EmailMessage


# amongst other things this will suppress those annoying logs
settings.DEBUG = False


class AreciboRunner(DjangoTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        super(AreciboRunner, self).setup_test_environment(**kwargs)
